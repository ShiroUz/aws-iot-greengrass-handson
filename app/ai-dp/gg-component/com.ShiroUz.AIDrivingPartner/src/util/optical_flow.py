import cv2
import numpy as np
import logging

logger = logging.getLogger("OpticalFlow")

class OpticalFlowAnalyzer:
    def __init__(self, threshold=5000):
        """
        Initialize the optical flow analyzer
        
        Args:
            threshold (int): Threshold for optical flow magnitude to detect near-miss incidents
        """
        self.prev_frame = None
        self.threshold = threshold
        self.stable_count = 0
        self.unstable_count = 0
        self.is_near_miss = False
        logger.info(f"Optical flow analyzer initialized with threshold: {threshold}")
    
    def reset(self):
        """Reset the analyzer state"""
        self.prev_frame = None
        self.stable_count = 0
        self.unstable_count = 0
        self.is_near_miss = False
    
    def analyze_frame(self, frame):
        """
        Analyze a frame using optical flow to detect near-miss incidents
        
        Args:
            frame: The current video frame (can be BGR or grayscale)
            
        Returns:
            tuple: (is_near_miss, is_stable, flow_magnitude, frame_with_flow)
                - is_near_miss: True if the current frame indicates a near-miss incident
                - is_stable: True if the driving is currently stable
                - flow_magnitude: The magnitude of the optical flow
                - frame_with_flow: The frame with optical flow visualization
        """
        # Convert frame to grayscale if needed
        if len(frame.shape) == 3:  # BGR frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:  # Already grayscale
            gray = frame
        
        # If this is the first frame, initialize and return
        if self.prev_frame is None:
            self.prev_frame = gray
            return False, True, 0, gray if len(frame.shape) == 2 else frame
        
        # Calculate optical flow using Farneback method
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_frame, gray, 
            None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Calculate magnitude and angle of flow
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        
        # Calculate total flow magnitude
        flow_magnitude = np.sum(magnitude)
        
        # Update previous frame
        self.prev_frame = gray
        
        # Create visualization
        frame_with_flow = self._visualize_flow(frame, flow, magnitude, angle)
        
        # Determine if this is a near-miss incident based on flow magnitude
        current_unstable = flow_magnitude > self.threshold
        
        # Update counters
        if current_unstable:
            self.stable_count = 0
            self.unstable_count += 1
            logger.info(f"Unstable motion detected! Flow: {flow_magnitude:.2f} > Threshold: {self.threshold}")
            if self.unstable_count >= 1:  # Reduced from 2 to 1 for faster detection
                self.is_near_miss = True
                logger.info("Near-miss condition triggered!")
        else:
            self.unstable_count = 0
            self.stable_count += 1
        
        # Determine stability (require 5 consecutive stable frames)
        is_stable = self.stable_count >= 5
        
        logger.info(f"Flow magnitude: {flow_magnitude:.2f}, Threshold: {self.threshold}, "
                   f"Near miss: {self.is_near_miss}, Stable: {is_stable}, "
                   f"Unstable count: {self.unstable_count}, Stable count: {self.stable_count}")
        
        return self.is_near_miss, is_stable, flow_magnitude, frame_with_flow
    
    def _visualize_flow(self, frame, flow, magnitude, angle):
        """Create a visualization of the optical flow"""
        # Handle grayscale input
        if len(frame.shape) == 2:  # Grayscale frame
            # Convert to BGR for visualization
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        else:
            frame_bgr = frame
            
        # Create HSV image for visualization
        hsv = np.zeros_like(frame_bgr)
        hsv[..., 1] = 255
        
        # Use angle for hue and normalized magnitude for value
        mag_max = np.max(magnitude) if np.max(magnitude) > 0 else 1
        hsv[..., 0] = angle * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        
        # Convert HSV to BGR
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Combine with original frame (50% transparent overlay)
        return cv2.addWeighted(frame_bgr, 0.7, bgr, 0.3, 0)
        
    def reset_near_miss_flag(self):
        """Reset the near-miss flag after handling an incident"""
        self.is_near_miss = False