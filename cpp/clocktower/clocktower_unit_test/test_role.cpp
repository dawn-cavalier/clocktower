#include "pch.h"
#include "CppUnitTest.h"
#include "../clocktower/src/globals/role.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace test_role
{
	TEST_CLASS(test_role)
	{
	public:
		TEST_METHOD(IsRoleTypes)
		{
			std::vector<Role> script{
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
				};

			Assert::IsTrue(is_townsfolk(Role::washerwoman));
			Assert::IsTrue(is_outsider(Role::drunk));
			Assert::IsTrue(is_minion(Role::poisoner));
			Assert::IsTrue(is_demon(Role::imp));
		}
	};
}
