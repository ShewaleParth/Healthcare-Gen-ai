"""
Pneumonia Detection System
Combines multiple models with Grad-CAM explainability
"""

import os
import torch
from pathlib import Path
from typing import Dict, List
import logging
from datetime import datetime

from app.models.efficientnet_model import PneumoniaEfficientNet
from app.utils.gradcam import GradCAM

logger = logging.getLogger(__name__)

class PneumoniaDetector:
    """Main pneumonia detection system with explainability"""
    
    def __init__(self, weights_dir: str = None):
        """
        Initialize pneumonia detector
        
        Args:
            weights_dir: Directory containing model weights
        """
        self.weights_dir = weights_dir or "weights"
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        logger.info(f"Initializing Pneumonia Detector on {self.device}")
        
        # Initialize models
        self.models = {}
        self._load_models()
        
        # Initialize Grad-CAM
        self.gradcam = None
        if 'efficientnet' in self.models:
            self._setup_gradcam()
    
    def _load_models(self):
        """Load all available models"""
        try:
            # Load EfficientNet-B0 (primary model)
            efficientnet_weights = os.path.join(self.weights_dir, 'efficientnet_pneumonia.pth')
            
            if os.path.exists(efficientnet_weights):
                self.models['efficientnet'] = PneumoniaEfficientNet(
                    weights_path=efficientnet_weights,
                    device=str(self.device)
                )
                logger.info("✅ Loaded EfficientNet-B0 with custom weights")
            else:
                # Use pre-trained ImageNet weights
                self.models['efficientnet'] = PneumoniaEfficientNet(device=str(self.device))
                logger.info("✅ Loaded EfficientNet-B0 with ImageNet weights")
            
            # TODO: Add DenseNet-121 and ResNet-50 here
            # self.models['densenet'] = PneumoniaDenseNet(...)
            # self.models['resnet'] = PneumoniaResNet(...)
            
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise
    
    def _setup_gradcam(self):
        """Setup Grad-CAM for explainability"""
        try:
            # Get the last convolutional layer
            target_layer = self.models['efficientnet'].model._conv_head
            self.gradcam = GradCAM(self.models['efficientnet'].model, target_layer)
            logger.info("✅ Grad-CAM initialized")
        except Exception as e:
            logger.warning(f"Grad-CAM setup failed: {e}")
    
    def predict(self, image_path: str) -> Dict:
        """
        Predict pneumonia from X-ray image
        
        Args:
            image_path: Path to X-ray image
            
        Returns:
            Prediction results with confidence and model breakdown
        """
        results = {
            'predictions': {},
            'ensemble': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Get predictions from all models
        for model_name, model in self.models.items():
            try:
                pred = model.predict(image_path)
                results['predictions'][model_name] = pred
                logger.info(f"{model_name}: {pred['prediction']} ({pred['confidence']:.2%})")
            except Exception as e:
                logger.error(f"{model_name} prediction failed: {e}")
                results['predictions'][model_name] = {'error': str(e)}
        
        # Calculate ensemble prediction
        results['ensemble'] = self._calculate_ensemble(results['predictions'])
        
        return results
    
    def _calculate_ensemble(self, predictions: Dict) -> Dict:
        """
        Calculate ensemble prediction from multiple models
        
        Args:
            predictions: Dictionary of model predictions
            
        Returns:
            Ensemble prediction
        """
        if not predictions:
            return {'error': 'No predictions available'}
        
        # Filter out failed predictions
        valid_preds = {k: v for k, v in predictions.items() if 'error' not in v}
        
        if not valid_preds:
            return {'error': 'All models failed'}
        
        # Simple averaging (can be weighted)
        pneumonia_probs = []
        normal_probs = []
        
        for pred in valid_preds.values():
            probs = pred.get('probabilities', {})
            pneumonia_probs.append(probs.get('PNEUMONIA', 0))
            normal_probs.append(probs.get('NORMAL', 0))
        
        avg_pneumonia = sum(pneumonia_probs) / len(pneumonia_probs)
        avg_normal = sum(normal_probs) / len(normal_probs)
        
        # Determine final prediction
        if avg_pneumonia > avg_normal:
            prediction = 'PNEUMONIA'
            confidence = avg_pneumonia
        else:
            prediction = 'NORMAL'
            confidence = avg_normal
        
        # Calculate agreement
        predictions_list = [p['prediction'] for p in valid_preds.values()]
        agreement = predictions_list.count(prediction)
        total = len(predictions_list)
        
        return {
            'prediction': prediction,
            'confidence': float(confidence),
            'probabilities': {
                'NORMAL': float(avg_normal),
                'PNEUMONIA': float(avg_pneumonia)
            },
            'agreement': f"{agreement}/{total}",
            'models_used': list(valid_preds.keys())
        }
    
    def generate_explainability(
        self,
        image_path: str,
        save_dir: str,
        prediction: str = None,
        confidence: float = None
    ) -> Dict:
        """
        Generate Grad-CAM visualization
        
        Args:
            image_path: Path to X-ray image
            save_dir: Directory to save visualizations
            prediction: Prediction label
            confidence: Confidence score
            
        Returns:
            Dictionary with paths to generated visualizations
        """
        if not self.gradcam:
            logger.warning("Grad-CAM not available")
            return {'error': 'Grad-CAM not initialized'}
        
        try:
            # Create save directory
            os.makedirs(save_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(save_dir, f"gradcam_{timestamp}.png")
            
            # Preprocess image
            input_tensor = self.models['efficientnet'].preprocess_image(image_path)
            
            # Generate and save Grad-CAM
            paths = self.gradcam.generate_and_save(
                input_tensor=input_tensor,
                original_image_path=image_path,
                save_path=save_path,
                prediction=prediction,
                confidence=confidence
            )
            
            logger.info(f"Grad-CAM visualization saved to {save_path}")
            return paths
            
        except Exception as e:
            logger.error(f"Grad-CAM generation failed: {e}")
            return {'error': str(e)}
    
    def analyze(self, image_path: str, save_dir: str = "uploads/heatmaps") -> Dict:
        """
        Complete analysis: prediction + explainability
        
        Args:
            image_path: Path to X-ray image
            save_dir: Directory to save visualizations
            
        Returns:
            Complete analysis results
        """
        # Get prediction
        results = self.predict(image_path)
        
        # Generate explainability
        ensemble = results.get('ensemble', {})
        if 'error' not in ensemble:
            gradcam_paths = self.generate_explainability(
                image_path=image_path,
                save_dir=save_dir,
                prediction=ensemble.get('prediction'),
                confidence=ensemble.get('confidence')
            )
            results['explainability'] = gradcam_paths
        
        return results

if __name__ == "__main__":
    # Test the detector
    detector = PneumoniaDetector()
    print("✅ Pneumonia Detector initialized successfully")
    print(f"Available models: {list(detector.models.keys())}")
    print(f"Grad-CAM available: {detector.gradcam is not None}")
