#include <stdint.h>
#include <string.h>

typedef struct {
    int x;
    int y;
} coord_t;


int get_stack(uint32_t *iboard, int rows, int cols, coord_t *stack) {
    int stack_size = 0;
    for (int row = 0; row < rows; row++) {
        for (int col = 0; col < cols; col++) {
            if (iboard[row * cols + col] > 1) {
                stack[stack_size++] = (coord_t) {row, col};
            }
        }
    }
    return stack_size;
}

void day21_step(uint32_t *iboard, uint32_t *oboard, int rows, int cols, int nsteps, uint32_t *results) {
    uint32_t steps[4][2] = {{0,  1},
                            {0,  -1},
                            {1,  0},
                            {-1, 0}};
    coord_t stack[100000];
    int stack_size = get_stack(iboard, rows, cols, stack);
    memcpy(iboard, oboard, rows*cols*sizeof(uint32_t));
    for (int i = 0; i < nsteps; i++) {
        for (int j = 0; j < stack_size; j++){
            for (int k = 0; k < 4; k++) {
                iboard[(stack[j].x + steps[k][0]) * cols + stack[j].y + steps[k][1]] *= 2;
            }
        }
        stack_size = get_stack(iboard, rows, cols, stack);
        results[i] = stack_size;
        memcpy(iboard, oboard, rows*cols*sizeof(uint32_t));
    }
}