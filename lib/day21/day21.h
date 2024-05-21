#include <stdint.h>

typedef struct {
    int x;
    int y;
} coord_t;

void day21_step(uint32_t *iboard, const uint32_t *oboard, int rows, int cols, int nsteps, uint32_t *results);