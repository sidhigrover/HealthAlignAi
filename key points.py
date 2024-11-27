import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

# Function to get keypoints from an image
def get_keypoints(image_path):
    # Read the image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to find the pose
    result = pose.process(image_rgb)

    # Check if keypoints are detected
    if result.pose_landmarks:
        keypoints = {}
        for id, lm in enumerate(result.pose_landmarks.landmark):
            keypoints[mp_pose.PoseLandmark(id).name] = (lm.x, lm.y)
        # Return both keypoints and image_rgb
        return keypoints, image_rgb
    else:
        print("Pose not detected")
        return None, None

# Example: Get keypoints from a specific image
image_path = "/content/1-0.png"  # Replace with your uploaded image file name
# Get keypoints and image_rgb
keypoints, image_rgb = get_keypoints(image_path)

# Display the keypoints dictionary
print(keypoints)

# Display the image
plt.imshow(cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()