#pragma once
#include <cstdint>
#include <vector>
#include <array>

#include "role.h"

enum class BasePlayerCount : uint8_t
{
	seven		= 0b0100,
	eight		= 0b0101,
	nine		= 0b0110,
	ten			= 0b1000,
	eleven		= 0b1001,
	twelve		= 0b1010,
	thirteen	= 0b1100,
	fourteen	= 0b1101,
	fifthteen	= 0b1110,
};

struct GameInfo
{
	std::array<Role, 31> script;
	BasePlayerCount base_player_count;
};

uint8_t get_townfolk_count(BasePlayerCount player_count);
uint8_t get_outsider_count(BasePlayerCount player_count);
uint8_t get_minion_count(BasePlayerCount player_count);
uint8_t get_demon_count(BasePlayerCount player_count);

std::vector<Role> get_townsfolk_from_script(std::array<Role, 31> script);
