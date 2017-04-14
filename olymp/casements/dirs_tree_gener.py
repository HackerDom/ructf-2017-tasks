import os
import os.path


class DirTreeCreator:
    def __init__(self, seed, path='./'):
        self._flags = []
        self._create_seed_flags(seed)
        self._root_dir_name = os.path.join(os.path.normpath(path), "un33d1060d33p3r")
        self.flag_files_info = []
        pass

    def _create_seed_flags(self, user_seed):
        gen = UniqueFlagsGenerator(user_seed)
        self._flags = [flag for flag in gen.flags_stream()]

    def _crete_dirs_from_path_list(self, to_write):
        # make_break
        to_write_dir_next = []
        to_write_file_next = []
        for path in to_write:
            os.makedirs(path, mode=0o755)
            head, tail = os.path.split(path)
            names = [rot for rot in self.name_rotations_stream(tail)]
            names.sort()
            for number, name in enumerate(names):
                path_next = os.path.join(path, name)
                if number in [1, 5]:
                    to_write_file_next.append(path_next)
                else:
                    to_write_dir_next.append(path_next)
        return to_write_dir_next, to_write_file_next

    def create_tree(self, path=''):
        path = os.path.normpath(path)
        path = os.path.join(path, self._root_dir_name)
        path = os.path.normpath(path)
        dirs = [path]
        length_files_to_write = 1
        files_to_write = []

        while length_files_to_write < 300:
            dirs_next, files = self._crete_dirs_from_path_list(dirs)
            dirs = dirs_next
            files_to_write = files_to_write + files
            length_files_to_write += len(files)

        for current_path, flag in zip(files_to_write, self._flags):
            head , tail = os.path.split(current_path)

            file_name = tail[::-1]
            file_name = file_name[:len(file_name) - 3] + flag[-3:]
            self.flag_files_info.append((file_name, flag))
            os.makedirs(current_path)
            file_path = os.path.join(current_path, file_name)
            f = open(file_path, 'x')
            f.write(flag)
            f.close()

    # @staticmethod
    def name_rotations_stream(self, name, rot=10):
        new_name = name + "".join([chr(code) for code in range(66, 66 + min(0, 10 - len(name)))])
        names = []
        for _ in range(0, rot):
            new_name = self.next_rot(new_name)
            names.append(new_name)
        for name in names:
            yield name

    @staticmethod
    def next_rot(name):
        return name[1:len(name)] + name[0:1]


class UniqueFlagsGenerator:
    def __init__(self, seed, amount=300):
        self._seed = seed
        self._amount = amount

    @staticmethod
    def _ends_stream():
        for code_1 in range(65, 69):
            for code_2 in range(97, 107):
                for code_3 in range(75, 85):
                    yield "{}{}{}".format(chr(code_1), chr(code_2), chr(code_3))

    @staticmethod
    def _trash_stream():
        for code_1 in range(85, 89):
            for code_2 in range(107, 117):
                for code_3 in [69, 70, 71, 72, 73, 74, 89, 90, 117, 118]:
                    yield "{}{}{}".format(chr(code_1), chr(code_2), chr(code_3))

    def _flag_content_stream(self):
        for flag_number in range(0, self._amount):
            flag_hash = (self._seed + 17 + flag_number) ** 19 * ((self._seed + 2 + flag_number) * 13)
            flag_string = str(flag_hash)
            yield flag_string[0: 28]

    def flags_stream(self):
        for flag_content, flag_trash, flag_end in zip(self._flag_content_stream(), self._trash_stream(),
                                                      self._ends_stream()):
            flag = "".join([symbol + flag_trash[(number + 2) % 3] + flag_end[(number + 1) % 3] for number, symbol in
                            enumerate(flag_content)])
            yield "RuCTF:" + flag + flag_end


if __name__ == "__main__":
    # uf = UniqueFlagsGenerator(1)
    dir_tree_creator = DirTreeCreator(2)
    dir_tree_creator.create_tree()
    for x in dir_tree_creator.flag_files_info:
        print(x)
    #for x in dir_tree_creator.name_rotations_stream("un33d1060d33p3r"):
    #    print(x)
