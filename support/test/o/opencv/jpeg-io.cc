#include <opencv2/opencv.hpp>

int main() {
    cv::Mat image = cv::imread("image.jpg", cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Could not open or find the image" << std::endl;
        return -1;
    }

    // Save the image as a JPEG file
    cv::imwrite("output.jpg", image);

    return 0;
}
