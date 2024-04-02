import cv2
import pytesseract
import multiprocessing
import time
from numba import jit
import os

@jit(nopython=True)
def ocr_worker(image, results):
    text = pytesseract.image_to_string(image)
    results.put(text)

def parallel_ocr(images, results):
    processes = []
    for image in images:
        process = multiprocessing.Process(target=ocr_worker, args=(image, results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    output_folder = "processed_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    results = multiprocessing.Queue()

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for better OCR results
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform OCR on the frame
        parallel_ocr([gray], results)

        # Process OCR results
        while not results.empty():
            text = results.get()
            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Save the processed image
        output_path = os.path.join(output_folder, f"processed_{int(time.time()*1000)}.jpg")
        cv2.imwrite(output_path, frame)

        # Display the frame
        cv2.imshow('OCR from Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    end_time = time.time()

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

    print(f"Total processing time: {(end_time - start_time)*1000:.2f} ms")
