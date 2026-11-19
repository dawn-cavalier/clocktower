#pragma once
#include <cstdint>
#include <vector>

#include "role.h"

/* TODO: This could be smaller! */
/* Invariant: Script Ends with Role::end */
typedef struct {
	std::vector<Role> script;
	uint8_t
		townsfolk_end,
		outsider_end,
		minion_end,
		demon_end,
		player_count,
		base_townsfolk_count,
		base_outsider_count,
		base_minion_count;
} GameInfo;
