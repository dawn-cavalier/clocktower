#include "role.h"

bool is_townsfolk(Role role)
{
	return Role::acrobat <= role && role <= Role::washerwoman;
}

bool is_outsider(Role role)
{
	return Role::barber <= role && role <= Role::zealot;
}

bool is_minion(Role role)
{
	return Role::assassin <= role && role <= Role::xaan;
}

bool is_demon(Role role)
{
	return Role::al_hadikhia <= role && role <= Role::zombuul;
}
