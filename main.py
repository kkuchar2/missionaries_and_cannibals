class State:

    def __init__(self, cannibal_count, missionairies_count, boat_state, previous_state):
        self.cannibal_count = cannibal_count
        self.missionairies_count = missionairies_count
        self.boat_state = boat_state
        self.previous_state = previous_state

    def __repr__(self):
        return "({} {} {})".format(self.cannibal_count, self.missionairies_count, self.boat_state)

    def __eq__(self, other):
        return self.missionairies_count == other.missionairies_count \
               and self.cannibal_count == other.cannibal_count \
               and self.boat_state == other.boat_state


def is_solution(state):
    return state.cannibal_count == 0 and state.missionairies_count == 0 and state.boat_state == 'P'


def expand_state(s, CANNIBAL_COUNT, MISSIONAIRIES_COUNT, BOAT_CAPACITY, already_visited):
    children = []

    if s.boat_state == 'L':  # If boat on the left side
        # All combinations of possible single fraction trips
        for n in range(0, BOAT_CAPACITY):
            if s.cannibal_count > n:
                state = State(s.cannibal_count - (n + 1), s.missionairies_count, 'P', s)
                if is_worth_visiting(state, already_visited, CANNIBAL_COUNT, MISSIONAIRIES_COUNT):
                    children.append(state)

            if s.missionairies_count > n:
                state = State(s.cannibal_count, s.missionairies_count - (n + 1), 'P', s)
                if is_worth_visiting(state, already_visited, CANNIBAL_COUNT, MISSIONAIRIES_COUNT):
                    children.append(state)

        # All combinations of possible mixed fraction trips
        for x in range(1, BOAT_CAPACITY):
            for y in range(1, BOAT_CAPACITY):
                if s.missionairies_count > x and s.cannibal_count > y and x + y <= BOAT_CAPACITY:
                    state = State(s.cannibal_count - x, s.missionairies_count - y, 'P', s)
                    if is_worth_visiting(state, already_visited, CANNIBAL_COUNT, MISSIONAIRIES_COUNT):
                        children.append(state)

    else:  # If boat on the right side
        # All combinations of possible single fraction trips
        for n in range(0, BOAT_CAPACITY):
            if MISSIONAIRIES_COUNT - s.cannibal_count > n:
                state = State(s.cannibal_count + (n + 1), s.missionairies_count, 'L', s)
                if is_worth_visiting(state, already_visited, CANNIBAL_COUNT, MISSIONAIRIES_COUNT):
                    children.append(state)

            if CANNIBAL_COUNT - s.missionairies_count > n:
                state = State(s.cannibal_count, s.missionairies_count + (n + 1), 'L', s)
                if is_worth_visiting(state, already_visited, CANNIBAL_COUNT, MISSIONAIRIES_COUNT):
                    children.append(state)

        # All combinations of possible mixed fraction trips
        for x in range(1, BOAT_CAPACITY):
            for y in range(1, BOAT_CAPACITY):
                if CANNIBAL_COUNT - s.cannibal_count > x and CANNIBAL_COUNT - s.missionairies_count > y \
                        and x + y <= BOAT_CAPACITY:
                    state = State(s.cannibal_count + x, s.missionairies_count + y, 'L', s)
                    if is_worth_visiting(state, already_visited, CANNIBAL_COUNT, MISSIONAIRIES_COUNT):
                        children.append(state)

    return children


def is_worth_visiting(state, already_visited, CANNIBAL_COUNT, MISSIONAIRIES_COUNT):
    if (state.cannibal_count > state.missionairies_count > 0) \
            or (CANNIBAL_COUNT - state.cannibal_count > MISSIONAIRIES_COUNT - state.missionairies_count > 0) \
            or state in already_visited:
        return False

    return True


def print_solution(final_state, CANNIBAL_COUNT, MISSIONAIRIES_COUNT, BOAT_CAPACITY):
    if final_state is None:
        print('No solution for CANNIBAL_COUNT = {} MISSIONAIRIES_COUNT = {} i BOAT_CAPACITY = {}.'
              .format(CANNIBAL_COUNT, MISSIONAIRIES_COUNT, BOAT_CAPACITY))
        return

    paths = []

    i = 1

    while final_state.previous_state is not None:
        c = final_state.cannibal_count
        m = final_state.missionairies_count
        b = final_state.boat_state

        pc = final_state.previous_state.cannibal_count
        pm = final_state.previous_state.missionairies_count
        pb = final_state.previous_state.boat_state

        previous_state_str = "({}, {}, {})".format(pc, pm, pb)
        next_state_str = "({}, {}, {})".format(c, m, b)
        roznica = "({}, {})".format(abs(pc - c), abs(pm - m))

        if i > 0:
            direction_str = "R"
        else:
            direction_str = "L"

        paths.append("{} + {}{} ---> {})".format(previous_state_str, direction_str, roznica, next_state_str))

        final_state = final_state.previous_state

        i = -i

    paths.reverse()

    print("Path:")

    for path in paths:
        print(path)

    print("----------------------------------------------------")
    print("Solution for (CANNIBAL_COUNT = {} MISSIONAIRIES_COUNT = {} i BOAT_CAPACITY = {}) exists."
          .format(CANNIBAL_COUNT, MISSIONAIRIES_COUNT, BOAT_CAPACITY))

    print("Number of boat trips: {}".format(len(paths)))


def missionairies_and_cannibals(CANNIBAL_COUNT=3, MISSIONAIRIES_COUNT=3, BOAT_CAPACITY=2):
    print("----------------------------------------------------")
    print("Cannibal count: {}, Missionairies count: {}, Boat capacity: {}"
          .format(CANNIBAL_COUNT, MISSIONAIRIES_COUNT, BOAT_CAPACITY))

    to_visit = []
    already_visited = []

    initial_state = State(CANNIBAL_COUNT, MISSIONAIRIES_COUNT, 'L', None)

    to_visit.append(initial_state)
    already_visited.append(initial_state)

    current_state = to_visit.pop(0)

    solution = None

    while True:

        if is_solution(current_state):
            solution = current_state
            break

        child_states = expand_state(current_state, CANNIBAL_COUNT, MISSIONAIRIES_COUNT, BOAT_CAPACITY, already_visited)

        to_visit.extend(child_states)
        already_visited.extend(child_states)

        if len(to_visit) == 0:
            break

        current_state = to_visit.pop(0)

    print_solution(solution, CANNIBAL_COUNT, MISSIONAIRIES_COUNT, BOAT_CAPACITY)


################################################################
missionairies_and_cannibals(3, 3, 2)
missionairies_and_cannibals(3, 3, 3)
missionairies_and_cannibals(4, 4, 2)
missionairies_and_cannibals(5, 5, 3)
missionairies_and_cannibals(2, 3, 2)
missionairies_and_cannibals(20, 20, 4)
################################################################
