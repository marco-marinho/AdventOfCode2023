#include <tuple>
#include <cstdint>
#include <vector>
#include <queue>
#include <set>
#include <utility>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

using std::tuple;
using std::vector;
using std::priority_queue;
using std::set;

typedef std::pair<int, int> point;

struct QueueEntry {
    uint64_t cost;
    point position;
    char direction;
    uint64_t count;

    QueueEntry(uint64_t cost, point movement, char direction, uint64_t count) :
    cost(cost), position(std::move(movement)), direction(direction), count(count) {};

    struct Compare {
        bool operator()(QueueEntry first, QueueEntry second) const{
            return first.cost > second.cost;
        }
    };

    class PQueue : public std::priority_queue<QueueEntry, std::vector<QueueEntry>, QueueEntry::Compare> {
    public:
        explicit PQueue(size_t reserve_size) {
            this->c.reserve(reserve_size);
        }
    };

};


static inline bool are_inverse(char a, char b) noexcept {
    return (a == 'r' && b == 'l') || (a == 'l' && b == 'r') ||
           (a == 'u' && b == 'd') || (a == 'd' && b == 'u');
}

static inline int to_int(char a) {
    switch (a) {
        case 'u':
            return 0;
        case 'd':
            return 1;
        case 'r':
            return 2;
        case 'l':
            return 3;
        default:
            return -1;
    }
}

template<size_t D, typename T>
struct NDVec : public vector<NDVec<D - 1, T>> {
  static_assert(D >= 1, "Vector dimension must be greater than zero!");
  template<typename... Args>
  explicit NDVec(size_t n = 0, Args... args) : vector<NDVec<D - 1, T>>(n, NDVec<D - 1, T>(args...)) {
  }
};
template<typename T>
struct NDVec<1, T> : public vector<T> {
  explicit NDVec(size_t n = 0, const T& val = T()) : vector<T>(n, val) {
  }
};

int djikstras(const py::array_t<uint64_t> &iboard, int min, int max) {
    static vector<tuple<point, char>> movements{{point(-1, 0), 'u'},
                                                {point(1, 0),  'd'},
                                                {point(0, 1),  'r'},
                                                {point(0, -1), 'l'}};
    auto board = iboard.unchecked<2>();
    QueueEntry::PQueue pq(500000);
    pq.emplace(board(0, 1), point(0, 1), 'r', 1);
    pq.emplace(board(1, 0), point(1, 0), 'd', 1);
    NDVec<4, bool> visited(board.shape(0), board.shape(1), 4, max + 1, false);
    while (!pq.empty()) {
        auto current = pq.top();
        auto [x, y] = current.position;
        pq.pop();
        if (visited[x][y][to_int(current.direction)][current.count]) {
            continue;
        }
        visited[x][y][to_int(current.direction)][current.count] = true;
        if (x == board.shape(0) - 1 && y == board.shape(1) - 1 && current.count >= min) {
            return static_cast<int>(current.cost);
        }
        for (auto [movement, direction]: movements) {
            auto [dx, dy] = movement;
            auto next_x = x + dx, next_y = y + dy;
            auto next_count = direction != current.direction ? 1 : current.count + 1;
            if ((current.count < min && current.direction != direction) ||
                are_inverse(current.direction, direction) ||
                next_count > max ||
                next_x < 0 || next_x >= board.shape(0) ||
                next_y < 0 || next_y >= board.shape(1)) {
                continue;
            }
            pq.emplace(current.cost + board(next_x, next_y),
                       point(next_x, next_y), direction, next_count);
        }
    }
    return -1;
}

PYBIND11_MODULE(day17_pybind, m) {
    m.def("native_djikstras", &djikstras, py::call_guard<py::gil_scoped_release>(), "Djikstras for Day 17");
}