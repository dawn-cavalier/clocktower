#pragma once
#include <cstdint>
#include <role.h>
enum Player : uint16_t
{
	one = 0x0001,
	two = 0x0002,
	three = 0x0004,
	four = 0x0008,
	five = 0x0010,
	six = 0x0020,
	seven = 0x0040,
	eight = 0x0080,
	nine = 0x0100,
	ten = 0x0200,
	eleven = 0x0400,
	twelve = 0x0800,
	thirteen = 0x1000,
	fourteen = 0x2000,
	fifthteen = 0x4000,
	storyteller = 0x8000,
};

enum class InfoType : uint8_t
{
	none,
	
	player_is_role_role_ping,
	player_is_alignment_alignment_ping,

	player_executed_ping,
	player_night_death_ping,
	player_day_death_ping,
	no_night_death,
	
	washerwoman_role_ping,
	librarian_role_ping,
	investigator_role_ping,
	chef_number,
	empath_number_ping,
	fortune_teller_check_ping,
	undertaker_ping,
	ravenkeeper_ping,
	virgin_trigger,
	virgin_execute,
	slayer_shot,
};

typedef struct Info
{
	uint16_t source;
	uint16_t day;
	float odds_sober;
} Info;

typedef struct RolePingInfo : Info
{
	uint16_t target_players;
	Role seen_role;
	uint8_t padding;
} RolePingInfo;

typedef struct AlignmentPingInfo : Info
{
	uint16_t target_players;
	bool is_good;
	uint8_t padding;
} AlignmentPingInfo;


typedef struct NumberInfo : Info
{
	uint8_t number, padding1, padding2, padding3;
} NumberInfo;

typedef struct NumberPingInfo : Info
{
	uint16_t target_players;
	uint8_t number, padding;
} NumberPingInfo;

typedef struct CheckPingInfo : Info
{
	uint16_t target_players;
	bool is_yes;
	uint8_t padding;
} CheckPingInfo;