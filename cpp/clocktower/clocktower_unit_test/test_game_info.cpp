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
				BasePlayerCount::seven
			};

			auto pointer = std::find(game_info.script.begin(), game_info.script.end(), Role::end);

			int index = std::distance(game_info.script.begin(), pointer);

			Assert::AreEqual(index, 22);
		}

		TEST_METHOD(PlayerCountMethods)
		{
			BasePlayerCount player_count = BasePlayerCount::seven;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 0);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 5);

			player_count = BasePlayerCount::eight;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 5);

			player_count = BasePlayerCount::nine;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 2);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 5);

			player_count = BasePlayerCount::ten;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 2);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 0);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 7);

			player_count = BasePlayerCount::eleven;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 2);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 7);

			player_count = BasePlayerCount::twelve;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 2);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 2);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 7);

			player_count = BasePlayerCount::thirteen;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 3);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 0);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 9);

			player_count = BasePlayerCount::fourteen;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 3);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 9);

			player_count = BasePlayerCount::fifthteen;
			Assert::AreEqual(static_cast<int>(get_demon_count(player_count)), 1);
			Assert::AreEqual(static_cast<int>(get_minion_count(player_count)), 3);
			Assert::AreEqual(static_cast<int>(get_outsider_count(player_count)), 2);
			Assert::AreEqual(static_cast<int>(get_townfolk_count(player_count)), 9);
		}

		TEST_METHOD(GetRolesFromScript)
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
				BasePlayerCount::seven
			};

			Assert::IsTrue(false);
		}

	};
}
