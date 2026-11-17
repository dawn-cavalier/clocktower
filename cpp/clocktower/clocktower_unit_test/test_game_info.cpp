#include "pch.h"
#include "CppUnitTest.h"
#include "../clocktower/src/globals/game_info.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace test_game_info
{
	TEST_CLASS(test_game_info)
	{
	public:
		
		TEST_METHOD(PlayerCountMethods)
		{
			BasePlayerCount player_count = BasePlayerCount::fifthteen;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 3);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 2);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 9);
		}
	};
}
