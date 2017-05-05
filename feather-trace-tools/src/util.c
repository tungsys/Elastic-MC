#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

#include "sched_trace.h"

static const char* event_names[] = {
	"INVALID",
        "NAME",
	"PARAM",
        "RELEASE",
	"ASSIGNED",
	"SWITCH_TO",
	"SWITCH_FROM",
	"COMPLETION",
	"BLOCK",
	"RESUME",
	"ACTION",
	"SYS_RELEASE",
	"NP_ENTER",
	"NP_EXIT",
	"INVALID"
};

const char* event2name(unsigned int id)
{
	if (id >= ST_INVALID)
		id = ST_INVALID;
	return event_names[id];
}


u64 event_time(struct st_event_record* rec)
{
	u64 when;
	switch (rec->hdr.type) {
		/* the time stamp is encoded in the first payload u64 */
	case ST_RELEASE:
	case ST_ASSIGNED:
	case ST_SWITCH_TO:
	case ST_SWITCH_AWAY:
	case ST_COMPLETION:
	case ST_BLOCK:
	case ST_RESUME:
	case ST_NP_ENTER:
	case ST_NP_EXIT:
	case ST_ACTION:
	case ST_SYS_RELEASE:
		when = rec->data.raw[0];
		break;
	default:
		/* stuff that doesn't have a time stamp should occur "early" */
		when = 0;
		break;
	};
	return when;
}

void print_header(struct st_trace_header* hdr)
{
	printf("%-14s %5u/%-5u on CPU%3u ",
	       event2name(hdr->type),
	       hdr->pid, hdr->job,
	       hdr->cpu);
}

typedef void (*print_t)(struct st_event_record* rec);

static void print_nothing(struct st_event_record* _)
{
}

static void print_raw(struct st_event_record* rec)
{
	printf(" type=%u", rec->hdr.type);
}

static void print_name(struct st_event_record* rec)
{
	/* terminate in all cases */
	rec->data.name.cmd[ST_NAME_LEN - 1] = 0;
	printf("%s", rec->data.name.cmd);
}

static void print_param(struct st_event_record* rec)
{
	printf("T=(cost:%6.2fms, period:%6.2fms, phase:%6.2fms), part=%d",
	       rec->data.param.wcet   / 1000000.0,
	       rec->data.param.period / 1000000.0,
	       rec->data.param.phase  / 1000000.0,\
	       rec->data.param.partition);
}

static void print_time_data2(struct st_event_record* rec)
{
	printf("%6.2fms", rec->data.raw[1] / 1000000.0);
}

static void print_action(struct st_event_record* rec)
{
	printf(" action=%u", rec->data.action.action);
}

static print_t print_detail[] = {
	print_raw,		/* invalid */
	print_name,		/* NAME  */
	print_param,		/* PARAM */
	print_time_data2,	/* RELEASE */
	print_nothing,		/* ASSIGNED */
	print_nothing,		/* SWITCH_TO */
	print_nothing,		/* SWITCH_FROM */
	print_nothing,		/* COMPLETION */
	print_nothing,		/* BLOCK */
	print_nothing,		/* RESUME */
	print_action,		/* ACTION */
	print_time_data2,	/* SYS_RELEASE */
	print_nothing,		/* NP_ENTER */
	print_nothing,		/* NP_EXIT */
	print_raw,		/* invalid */
};

void print_event(struct st_event_record *rec)
{
	unsigned int id = rec->hdr.type;

	/* ensure there's a handler for each ID */
	assert(sizeof(print_detail) / sizeof(print_detail[0]) == ST_INVALID + 1);

	if (id >= ST_INVALID)
		id = ST_INVALID;
	print_header(&rec->hdr);
	print_detail[id](rec);
	printf("\n");
}

void print_all(struct st_event_record *rec, unsigned int count)
{
	unsigned int i;
	for (i = 0; i < count; i++)
		print_event(&rec[i]);
}
