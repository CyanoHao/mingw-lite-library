#include <opencv2/opencv.hpp>

void test_imread(const std::string &filename) {
  cv::Mat image = cv::imread(filename, cv::IMREAD_COLOR);

  if (image.empty()) {
    std::cerr << "Could not load image: " << filename << std::endl;
    exit(EXIT_FAILURE);
  }

  std::cout << "Image size: " << image.size() << std::endl;

  auto px_0 = image.at<cv::Vec3b>(0, 0);
  std::cout << "Black pixel ok: " << (px_0[0] < 8 && px_0[1] < 8 && px_0[2] < 8) << std::endl;

  auto px_1 = image.at<cv::Vec3b>(0, 1);
  std::cout << "White pixel ok: " << (px_1[0] > 248 && px_1[1] > 248 && px_1[2] > 248) << std::endl;
}

int main() {
  test_imread("grid.jpg");
  test_imread("grid.png");
  test_imread("grid.webp");

  return 0;
}
