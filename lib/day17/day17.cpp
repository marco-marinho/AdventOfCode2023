#include <tuple>
#include <utility>
#include <cstdint>
#include <vector>
#include <queue>
#include <set>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

using std::tuple;
using std::vector;
using std::array;
using std::priority_queue;
using std::set;

typedef tuple<int, int> step;

struct QueueEntry {
    uint64_t cost;
    step position;
    char direction;
    uint64_t count;

    QueueEntry(uint64_t cost, step movement, char direction, uint64_t count) :
            cost(cost), position(std::move(movement)), direction(direction), count(count) {};

    bool operator<(const QueueEntry &other) const {
        return std::tie(position, direction, count) < std::tie(other.position, other.direction, other.count);
    }
};

class CompareQueueEntry {
public:
    bool operator()(QueueEntry first, QueueEntry second) {
        return first.cost > second.cost;
    }
};

static inline bool are_inverse(char a, char b) noexcept {
    return (a == 'r' && b == 'l') || (a == 'l' && b == 'r') ||
           (a == 'u' && b == 'd') || (a == 'd' && b == 'u');
}

int djikstras(const py::array_t<uint64_t> &iboard, int min, int max) {
    auto board = iboard.unchecked<2>();
    priority_queue<QueueEntry, std::vector<QueueEntry>, CompareQueueEntry> pq;
    pq.emplace(board(0, 1), step(0, 1), 'r', 1);
    pq.emplace(board(1, 0), step(1, 0), 'd', 1);
    vector<tuple<step, char>> movements{{step(-1, 0), 'u'},
                                        {step(1, 0),  'd'},
                                        {step(0, 1),  'r'},
                                        {step(0, -1), 'l'}};
    set<QueueEntry> visited;
    while (!pq.empty()) {
        auto current = pq.top();
        pq.pop();
        if (visited.find(current) != visited.end()) {
            continue;
        }
        visited.emplace(current);
        auto [x, y] = current.position;
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
            pq.emplace(current.cost + board(next_x, next_y), step(next_x, next_y), direction, next_count);
        }
    }
    return -1;
}

PYBIND11_MODULE(day17_pybind, m) {
    m.def("native_djikstras", &djikstras, py::call_guard<py::gil_scoped_release>(), "Djikstras for Day 17");
}