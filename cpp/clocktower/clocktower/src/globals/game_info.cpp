#include "game_info.h"

uint8_t get_base_townfolk_count(BasePlayerCount player_count)
{
    uint8_t minion_count = static_cast<uint8_t>(player_count) & 0b1100;
    minion_count = minion_count >> 2;
    uint8_t townsfolk_count = (minion_count << 1) + 3;
    return townsfolk_count;
}

uint8_t get_base_outsider_count(BasePlayerCount player_count)
{
    uint8_t outsider_count = static_cast<uint8_t>(player_count) & 0b0011;
    return outsider_count;
}

uint8_t get_base_minion_count(BasePlayerCount player_count)
{
    uint8_t minion_count = static_cast<uint8_t>(player_count) & 0b1100;
    minion_count = minion_count >> 2;
    return minion_count;
}

uint8_t get_base_demon_count(BasePlayerCount player_count)
{
    return 1;
}
