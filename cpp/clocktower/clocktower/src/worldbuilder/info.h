#pragma once
#include <cstdint>
#include <array>

#include "../globals/role.h"

enum class OtherInfoBitMask: uint8_t
{
	is_yes	= 0b10000000,
	is_good = 0b01000000,
	number	= 0b00111111,
};

typedef struct Info
{
	//InfoType info_type;
	float odds_sober;
	std::array<Role, 2> seen_roles;
	uint16_t target_players;
	uint16_t source;
	uint8_t day;
	uint8_t other_info;
};
