"""
Grad-CAM (Gradient-weighted Class Activation Mapping) Implementation
Provides visual explainability for pneumonia detection
"""

import torch
import torch.nn.functional as F
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class GradCAM:
    """Grad-CAM implementation for model explainability"""
    
    def __init__(self, model, target_layer):
        """
        Initialize Grad-CAM
        
        Args:
            model: PyTorch model
            target_layer: Layer to visualize (usually last conv layer)
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.register_hooks()
    
    def register_hooks(self):
        """Register forward and backward hooks"""
        
        def forward_hook(module, input, output):
            self.activations = output.detach()
        
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()
        
        # Register hooks on target layer
        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)
    
    def generate_cam(self, input_tensor: torch.Tensor, target_class: int = None) -> np.ndarray:
        """
        Generate Class Activation Map
        
        Args:
            input_tensor: Input image tensor
            target_class: Target class index (None for predicted class)
            
        Returns:
            CAM heatmap as numpy array
        """
        # Forward pass
        self.model.zero_grad()
        output = self.model(input_tensor)
        
        # Get target class
        if target_class is None:
            target_class = output.argmax(dim=1).item()
        
        # Backward pass
        one_hot = torch.zeros_like(output)
        one_hot[0][target_class] = 1
        output.backward(gradient=one_hot, retain_graph=True)
        
        # Get gradients and activations
        gradients = self.gradients[0]  # (C, H, W)
        activations = self.activations[0]  # (C, H, W)
        
        # Calculate weights (global average pooling of gradients)
        weights = gradients.mean(dim=(1, 2), keepdim=True)  # (C, 1, 1)
        
        # Weighted combination of activation maps
        cam = (weights * activations).sum(dim=0)  # (H, W)
        
        # Apply ReLU
        cam = F.relu(cam)
        
        # Normalize to [0, 1]
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)
        
        # Convert to numpy
        cam = cam.cpu().numpy()
        
        return cam
    
    def create_heatmap(self, cam: np.ndarray, original_image_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Create heatmap visualization
        
        Args:
            cam: Class activation map
            original_image_path: Path to original image
            
        Returns:
            Tuple of (heatmap, overlay, original_image)
        """
        # Load original image
        original_image = cv2.imread(original_image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        h, w = original_image.shape[:2]
        
        # Resize CAM to match original image size
        cam_resized = cv2.resize(cam, (w, h))
        
        # Apply colormap (JET colormap: blue=low, red=high)
        heatmap = cm.jet(cam_resized)[:, :, :3]  # Remove alpha channel
        heatmap = (heatmap * 255).astype(np.uint8)
        
        # Create overlay
        overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)
        
        return heatmap, overlay, original_image
    
    def save_visualization(
        self,
        heatmap: np.ndarray,
        overlay: np.ndarray,
        original: np.ndarray,
        save_path: str,
        prediction: str = None,
        confidence: float = None
    ):
        """
        Save Grad-CAM visualization
        
        Args:
            heatmap: Heatmap image
            overlay: Overlay image
            original: Original image
            save_path: Path to save visualization
            prediction: Prediction label (optional)
            confidence: Confidence score (optional)
        """
        # Create figure with 3 subplots
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Original image
        axes[0].imshow(original)
        axes[0].set_title('Original X-Ray', fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        # Heatmap
        axes[1].imshow(heatmap)
        axes[1].set_title('Grad-CAM Heatmap\n(Red = High Importance)', fontsize=12, fontweight='bold')
        axes[1].axis('off')
        
        # Overlay
        axes[2].imshow(overlay)
        title = 'Overlay Visualization'
        if prediction and confidence:
            title += f'\n{prediction} ({confidence:.1%})'
        axes[2].set_title(title, fontsize=12, fontweight='bold')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualization saved to {save_path}")
    
    def generate_and_save(
        self,
        input_tensor: torch.Tensor,
        original_image_path: str,
        save_path: str,
        target_class: int = None,
        prediction: str = None,
        confidence: float = None
    ) -> dict:
        """
        Generate Grad-CAM and save visualization (all-in-one)
        
        Args:
            input_tensor: Input image tensor
            original_image_path: Path to original image
            save_path: Path to save visualization
            target_class: Target class index
            prediction: Prediction label
            confidence: Confidence score
            
        Returns:
            Dictionary with paths to generated images
        """
        # Generate CAM
        cam = self.generate_cam(input_tensor, target_class)
        
        # Create heatmap
        heatmap, overlay, original = self.create_heatmap(cam, original_image_path)
        
        # Save visualization
        self.save_visualization(heatmap, overlay, original, save_path, prediction, confidence)
        
        # Also save individual images
        base_path = save_path.rsplit('.', 1)[0]
        heatmap_path = f"{base_path}_heatmap.png"
        overlay_path = f"{base_path}_overlay.png"
        
        cv2.imwrite(heatmap_path, cv2.cvtColor(heatmap, cv2.COLOR_RGB2BGR))
        cv2.imwrite(overlay_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
        
        return {
            'combined': save_path,
            'heatmap': heatmap_path,
            'overlay': overlay_path
        }

if __name__ == "__main__":
    print("✅ Grad-CAM module ready")
