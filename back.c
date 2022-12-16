#include <definitions.h>

#include <stdio.h>
#include <stdlib.h>

task_t **task_list = NULL;
int task_elements = 0;

void (*schedulers[SCHED_MAX])();

void create_task(uint8_t priority, time_t due, uint64_t uuid)
{
	if (task_list == NULL) {
		printf("Error, no task list is NULL\n");
		return;
	}

	task_t *task = (task_t *)malloc(sizeof(task_t));
	task->priority = priority;
	task->due_date = due;
	task->uuid = uuid;
	task_list[task_elements - 1] = task;

	task_list = (task_t **)realloc(task_list, (++task_elements) * sizeof(task_t));
}

void edit_task(int i, uint8_t priority, time_t due, uint64_t uuid)
{
	task_list[i]->priority = priority;
	task_list[i]->due_date = due;
	task_list[i]->uuid = uuid;
}

void bubble_sort()
{
    for (int i = 0; i < task_elements - 1; i++) {
        for (int j = 0; j < task_elements - 2; j++) {
            if (task_list[j] != NULL & task_list[j + 1] != NULL) {
                task_t *tmp = task_list[j];
                if (task_list[j]->priority > task_list[j + 1]->priority) {
                    task_list[j] = task_list[j + 1];
                    task_list[j + 1] = tmp;
                }
            }
        }
    }

    for (int i = 0; i < task_elements - 1; i++) {
        for (int j = 0; j < task_elements - 2; j++) {
            if (task_list[j] != NULL & task_list[j + 1] != NULL) {
                task_t *tmp = task_list[j];
                if (task_list[j]->due_date > task_list[j + 1]->due_date) {
                    task_list[j] = task_list[j + 1];
                    task_list[j + 1] = tmp;
                }
            }
        }
    }
}

void delete_task(int i)
{
	free(task_list[i]);
	task_list[i] = NULL;
}


// py_load - Python handles serializtion and data loading (init)
void initalize(char *file)
{
	if (file == NULL) {
		printf("Save file was NULL, loading blank user and task list\n");

		task_list = (task_t **)malloc(sizeof(task_t));
		task_elements = 1;

		return;
	}


	/* Load following data into respective structures:
	 *	-> Tasks
	 * 	-> User
	 */
}

uint64_t get_task(int i)
{
	if (task_list[i] == NULL)
		return 0;

	return task_list[i]->uuid;
}

int get_task_list_size()
{
	return task_elements - 1;
}

void initalize_schedulers()
{
	schedulers[SCHED_BUBBLE_SORT] = bubble_sort;
}

void call_scheduler(int idx)
{
	(*schedulers[idx])();
}

// Python:
// A, B, C, D
// 1, 2, 3, 4
// C:
// C, B, A, D
// 3, 2, 1, 4
// Python:
// [0]       [1]       [2]        [3]
// tasks[3] tasks[2]  tasks[1]   tasks[4]
//  C         B         A          D
