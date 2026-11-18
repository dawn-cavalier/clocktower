#include "pch.h"
#include "CppUnitTest.h"
#include "../clocktower/src/globals/game_info.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace test_game_info
{
	TEST_CLASS(test_game_info)
	{
	public:
		TEST_METHOD(GameInfoConstruction)
		{
			GameInfo game_info{
				{
					Role::washerwoman,
					Role::librarian,
					Role::investigator,
					Role::chef,
					Role::empath,
					Role::fortune_teller,
					Role::undertaker,
					Role::monk,
					Role::ravenkeeper,
					Role::virgin,
					Role::slayer,
					Role::soldier,
					Role::mayor,
					Role::butler,
					Role::drunk,
					Role::recluse,
					Role::saint,
					Role::poisoner,
					Role::spy,
					Role::scarlet_woman,
					Role::baron,
					Role::imp,
					Role::end,
				},
				13,
				17,
				21,
				22,
				7,
				5,
				0,
				1,
			};

			auto pointer = std::find(game_info.script.begin(), game_info.script.end(), Role::end);

			int index = std::distance(game_info.script.begin(), pointer);

			Assert::IsTrue(index == game_info.demon_end);
		}
	};
}
