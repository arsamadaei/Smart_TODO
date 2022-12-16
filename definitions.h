#ifndef DEFINITIONS_H
#define DEFINITIONS_H

#include <stdint.h>
#include <time.h>

struct task
{
    // Inputs
    uint8_t priority;
    time_t due_date;
    uint64_t uuid;
};
typedef struct task task_t;

enum schedulers
{
    // "SCHED_" + Name of the scheduler
    SCHED_BUBBLE_SORT,

    SCHED_MAX,
};

extern task_t **task_list;
extern int task_elements;

void create_task(uint8_t priority, time_t due, uint64_t uuid);

void initalize(char *file);

#endif
