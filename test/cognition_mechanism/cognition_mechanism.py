from legal_reward_hacking import learn_norm, update_norm_base


def test_learn_norm():
    character_profile = {
        "name": "张三",
        "age": 16,
        "gender": "男",
        "education": "本科",
        "profession": "程序员",
        "income": 10000,
        "temperament": "暴躁、冲动",
        "hobby": "喝酒"
    }
    environment_setting = {
        "backgound": "A国a城市。其中有很多无许可证的酒馆。里面有不少年轻人买酒喝。没有人监管"
    }
    new_norm = "禁止未成年人饮酒"
    self_norm = learn_norm([], character_profile, environment_setting, new_norm)
    print(self_norm)


def test_update_norm_base():
    norm_base = ["我是未成年人，我怕被抓，所以不能自己去酒吧喝酒"]
    character_profile = {
        "name": "张三",
        "age": 16,
        "gender": "男",
        "education": "本科",
        "profession": "程序员",
        "income": 10000,
        "temperament": "暴躁、冲动",
        "hobby": "喜欢喝酒"
    }
    environment_setting = {
        "backgound": "A国a城市。其中有很多无许可证的酒馆。里面有不少年轻人买酒喝。没有人监管"
    }
    feedback = {
        "bartender's word": "未成年人也可以随便买酒喝",
        "police's word": "我们不会管未成年人买酒喝"
    }
    new_norm_base = update_norm_base(norm_base, character_profile, environment_setting, feedback)
    print(new_norm_base)


if __name__ == "__main__":
    test_learn_norm()
    # test_update_norm_base()
