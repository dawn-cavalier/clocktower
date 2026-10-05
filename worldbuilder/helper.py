from worldbuilder.evilTeamInfo import EvilTeamInfo


def get_info_trust(info_indices: list[int], learned_info: list[EvilTeamInfo]):
    trust_score = 1.0

    for info_index in info_indices:
        is_inverted = info_index < 0
        info = learned_info[abs(info_index)]
        if is_inverted:
            trust_score = trust_score * (1.0 - info.info_trust)
        else:
            trust_score = trust_score * info.info_trust

    return trust_score
