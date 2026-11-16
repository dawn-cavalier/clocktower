#pragma once
#include <cstdint>
#include "role.h"

enum class BasePlayerCount : uint8_t
{
	seven		= 0b0000,
	eight		= 0b0001,
	nine		= 0b0010,
	ten			= 0b0100,
	eleven		= 0b0101,
	twelve		= 0b0110,
	thirteen	= 0b1000,
	fourteen	= 0b1001,
	fifthteen	= 0b1010,
};

struct GameInfo
{
	BasePlayerCount base_player_count;
	Role* script[];
};
