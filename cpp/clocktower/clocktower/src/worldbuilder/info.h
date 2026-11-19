#pragma once
#include <cstdint>
enum class Player : uint16_t
{
	one			= 0x0001,
	two			= 0x0002,
	three		= 0x0004,
	four		= 0x0008,
	five		= 0x0010,
	six			= 0x0020,
	seven		= 0x0040,
	eight		= 0x0080,
	nine		= 0x0100,
	ten			= 0x0200,
	eleven		= 0x0400,
	twelve		= 0x0800,
	thirteen	= 0x1000,
	fourteen	= 0x2000,
	fifthteen	= 0x4000,
};

enum class InfoType : uint8_t
{
	none,
};

typedef struct
{
	uint16_t target_players;
	uint16_t source;
	InfoType info_type;
	uint8_t day;
	uint8_t number;
	bool is_yes;
	bool is_good;
} Info;
