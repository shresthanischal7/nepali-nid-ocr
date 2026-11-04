import cv2
import numpy as np

class PerspectiveCorrector:
    
    def __init__(self, image):
        self.image = image
        self.gray = None
        self.img_blur = None
        self.img_canny = None
        self.img_thresh = None
        self.img_dilation = None
        self.img_erosion = None

        self.contours = None
        self.points = None
        self.warped_img = None
        self.largest_contour = None
    
    @staticmethod
    def reorder(points):
        points_new = np.zeros_like(points)
        points = points.reshape((4,2))
        
        add = np.sum(points, axis=1)
        points_new[0] = points[np.argmin(add)]
        points_new[3] = points[np.argmax(add)]
        
        diff = np.diff(points, axis=1)
        points_new[1] = points[np.argmin(diff)]
        points_new[2] = points[np.argmax(diff)]
        
        return points_new
    
    def grayscale(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return self.gray
    
    def gaussian_blur(self):
        if self.gray is None:
            raise ValueError('First make the image grayscaled.')
        self.img_blur = cv2.GaussianBlur(
            self.gray, 
            (5,5),
            0
            )
        return self.img_blur
    
    def canny_edges(self):
        if self.img_blur is None:
            raise ValueError("Apply Gaussian blur first.")

        self.img_canny = cv2.Canny(
            self.img_blur,
            50, 
            150
        )

        return self.img_canny
    
    def threshold(self):
        if self.img_blur is None:
            raise ValueError("Apply Gaussian blur first.")

        _, self.img_thresh = cv2.threshold(
            self.img_blur,
            0,  
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return self.img_thresh
    
    
    def dilation(self):
        if self.img_thresh is None:
            raise ValueError("Apply thresholding first.")

        kernel = np.ones((3, 3), dtype=np.uint8)

        self.img_dilation = cv2.dilate(
            self.img_thresh,
            kernel,
            iterations=1
        )

        return self.img_dilation
    
    def erosion(self):
        if self.img_dilation is None:
            raise ValueError("Apply dilation first.")
        
        kernel = np.ones((3, 3), dtype=np.uint8)
        
        self.img_erosion = cv2.erode(
            self.img_dilation,
            kernel,
            iterations=1
        )
        
        return self.img_erosion
    
    def find_contours(self):
        if self.erosion is None:
            raise ValueError("Apply erossion first")

        self.contours , _ = cv2.findContours(
            self.img_erosion,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        return self.contours


    def find_largest_contour(self):
        if self.contours is None:
            raise ValueError("Find contours first.")

        if len(self.contours) == 0:
            raise ValueError("No contours detected.")

        sorted_contours = sorted(
            self.contours,
            key=cv2.contourArea,
            reverse=True
        )

        for contour in sorted_contours:

            area = cv2.contourArea(contour)

            perimeter = cv2.arcLength(contour, True)

            approx = cv2.approxPolyDP(
                contour,
                0.02 * perimeter,
                True
            )

            if len(approx) == 4:
                self.largest_contour = contour
                self.points = approx
                return self.largest_contour

        raise ValueError("No quadrilateral contour found.")
    
    def approximate_contour(self):
        if self.largest_contour is None:
            raise ValueError('First find the largest contour')
        
        perimeter = cv2.arcLength(self.largest_contour, True)
        
        self.points = cv2.approxPolyDP(
            self.largest_contour,
            0.02 * perimeter,
            True
        )
        
        return self.points

    def draw_contours(self):
        if self.contours is None:
            raise ValueError("Find contours first.")

        contour_image = self.image.copy()

        cv2.drawContours(
            contour_image,
            self.contours,
            -1,
            (0, 255, 0),
            2
        )

        return contour_image
    
    def inspect_contours(self):
        if self.contours is None:
            raise ValueError('Find contour first')

        sorted_contours = sorted(
            self.contours,
             key=cv2.contourArea,
             reverse=True
        )
        
        for i , contour in enumerate(sorted_contours[:5]):
            area = cv2.contourArea(contour)
            
            perimeter = cv2.arcLength(contour, True)

            approx = cv2.approxPolyDP(
                contour,
                0.02 * perimeter,
                True
            )

            print(f"\nContour {i + 1}")
            print("Area:", area)
            print("Number of points:", len(approx))
            print("Approximated coordinates:\n", approx) 
            
    def correct_perspective(self):
            
            """ Sends a wraped image that fixes the perspective """
            self.grayscale()
            self.gaussian_blur()
            self.threshold()
            self.dilation()
            self.erosion()
            
            self.find_contours()
            self.find_largest_contour()
            
            self.approximate_contour()
            
            self.points = self.reorder(self.points)
            
            self.warped_img = self.perspective_transform(self.points)
            
            self.image = self.warped_img
            
            # return cv2.cvtColor(self.warped_img, cv2.COLOR_BGR2GRAY)
            
            return self.warped_img
            
    @staticmethod
    def calculate_dimensions(points):

        points = points.reshape(4, 2)

        tl, tr, bl, br = points

        width_top = np.linalg.norm(tr - tl)
        width_bottom = np.linalg.norm(br - bl)

        height_left = np.linalg.norm(bl - tl)
        height_right = np.linalg.norm(br - tr)

        width = int(max(width_top, width_bottom))
        height = int(max(height_left, height_right))

        return width, height
    
    def perspective_transform(self, points):
        width, height = self.calculate_dimensions(points)

        # Destination corner coordinates
        destination_points = np.float32([
            [0, 0],                  # Top-left
            [width - 1, 0],          # Top-right
            [0, height - 1],         # Bottom-left
            [width - 1, height - 1]  # Bottom-right
        ])

        # Convert source points to the required format
        source_points = np.float32(points.reshape(4, 2))

        # Calculate perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(
            source_points,
            destination_points
        )

        # Apply perspective transformation
        self.warped_img = cv2.warpPerspective(
            self.image,
            matrix,
            (width, height)
        )

        return self.warped_img