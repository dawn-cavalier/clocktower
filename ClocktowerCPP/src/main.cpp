#include <iostream>
#include <SDL3/SDL.h>

int main(int argc, char* argv[])
{
	if (!SDL_Init(SDL_INIT_VIDEO))
	{
		std::cout << "Error initializing sdl3\n";
	}
	return 0;
}