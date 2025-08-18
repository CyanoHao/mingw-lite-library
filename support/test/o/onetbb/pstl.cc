#include <algorithm>
#include <execution>
#include <iostream>
#include <vector>

int main() {
  constexpr int N = 1'000'000;
  std::vector<int> v;
  v.reserve(N);
  for (int i = 0; i < N; ++i)
    v.push_back(i);

  std::sort(std::execution::par, v.begin(), v.end());

  bool sorted = true;
  for (int i = 1; i < N; ++i) {
    if (v[i] < v[i - 1]) {
      sorted = false;
      break;
    }
  }

  if (sorted)
    std::cout << "sorted" << std::endl;
  else
    std::cout << "not sorted" << std::endl;
}
