import cv2
import numpy as np

HEIGHT = 1080
WIDTH = 1920


# Tear line for horizontal tearing
HORIZONTAL_TEAR_LINE = int(HEIGHT * 0.5)

# Tear line for vertical tearing
VERTICAL_TEAR_LINE = int(WIDTH * 0.65)

# Create a triangular mask for diagonal tearing
diag_mask = np.tri(HEIGHT, WIDTH, int(WIDTH * 0.15), dtype=np.uint8)
diag_mask = np.expand_dims(diag_mask, axis=-1) * np.ones(3, dtype=np.uint8)


def load_video(video_path: str) -> cv2.VideoCapture:
    # Load video
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    return cap  # Return the video capture object


def start_video_writer(out_path: str) -> cv2.VideoWriter:
    # Set up the output video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4 format
    frame_rate = 30  # Adjust according to your video's frame rate
    out = cv2.VideoWriter(out_path, fourcc, frame_rate, (WIDTH, HEIGHT))

    return out  # Return the video capture object


def diagonal_tearing(prev_frame, curr_frame) -> np.ndarray:
    # Apply the mask to create diagonal tearing
    torn_frame = prev_frame * diag_mask + curr_frame * (1 - diag_mask)
    return torn_frame


def horizontal_tearing(
    prev_frame, curr_frame, h_tear_line=HORIZONTAL_TEAR_LINE
) -> np.ndarray:
    top_half = prev_frame[:h_tear_line, :]
    bottom_half = curr_frame[h_tear_line:, :]
    return np.vstack((top_half, bottom_half))


def vertical_tearing(
    prev_frame, curr_frame, v_tear_line=VERTICAL_TEAR_LINE
) -> np.ndarray:
    left_half = prev_frame[:, :v_tear_line]
    right_half = curr_frame[:, v_tear_line:]
    return np.hstack((left_half, right_half))


def tearing_simulation(
    tearing_type: str,
    cap: cv2.VideoCapture,
    out: cv2.VideoWriter = None,
    show: bool = False,
):

    # Read the first frame and resize it
    ret, prev_frame = cap.read()
    if ret:
        prev_frame = cv2.resize(prev_frame, (WIDTH, HEIGHT))

    # Create a triangular mask for diagonal tearing
    # Adjust the parameters for different angles of tearing

    # Process video
    while cap.isOpened():
        # Read next frame
        ret, curr_frame = cap.read()
        if not ret:
            break

        # Resize the current frame
        curr_frame = cv2.resize(curr_frame, (WIDTH, HEIGHT))

        # # Apply the mask to create diagonal tearing
        # if tearing_type == "diagonal":
        #     torn_frame = diagonal_tearing(prev_frame, curr_frame)
        # elif tearing_type == "horizontal":
        #     torn_frame = horizontal_tearing(prev_frame, curr_frame)
        # elif tearing_type == "vertical":
        #     torn_frame = vertical_tearing(prev_frame, curr_frame)
        # else:
        #     print("Error: Invalid tearing type.")
        #     exit()
        torn_frame = curr_frame
        # Display torn frame
        if show:
            cv2.imshow("Tearing Simulation", torn_frame)

        # Write the frame to the output video
        if out:
            out.write(torn_frame)

        # Set the current frame as the previous frame for the next iteration
        prev_frame = curr_frame

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release everything if job is finished

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # tearing_type = "diagonal"
    # tearing_type = "vertical"
    tearing_type = "horizontal"

    # For window tearing
    video_path = "/home/fernando/Videos/Screencasts/window_screencast.webm"
    out_path = f"/home/fernando/Videos/Screencasts/original/no_tearing_{tearing_type}.mp4"

    # For line tearing
    # video_path = "/home/fernando/Videos/Screencasts/moving_vertical_lines.mp4"
    # out_path = f"/home/fernando/Videos/Screencasts/out/line_tearing_{tearing_type}.mp4"

    cap = load_video(video_path)
    out = start_video_writer(out_path)

    tearing_simulation(tearing_type, cap, out, show=False)

    cap.release()
    if out:
        out.release()
