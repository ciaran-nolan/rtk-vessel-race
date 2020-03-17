
import interpolation
import ubx_messages
import relpos_sim_data
import matplotlib.pyplot as plt
import classes
base_ned = ubx_messages.FinishPin(8000, 6000)


def simulation():
    base1, boat_history1, extracted_data1 = relpos_sim_data.variable_speeds()
    base2, boat_history2, extracted_data2 = relpos_sim_data.variable_speed_straight_line()
    base3, boat_history3, extracted_data3 = relpos_sim_data.variable_speed_single_quadratic()
    base4, boat_history4, extracted_data5 = relpos_sim_data.upwind_tacks()
    base5, boat_history5, extracted_data6 = relpos_sim_data.generate_tight_tack()
    base5, boat_history5, extracted_data6 = relpos_sim_data.generate_slow_turn()

    base = classes.base(base1)

    print("Full data approximation: ")
    interpolation.linear_interpolation_shortest_distance(base, boat_history1, True)
    print("Extracted Data Linear Approximation: ")
    interpolation.linear_interpolation_shortest_distance(base, extracted_data1, True)
    print("Extracted Data Non-Linear Approximation")
   # interpolation.nonlinear_interpolation_shortest_distance(base1, extracted_data1)
    #interpolation.nonlinear_interpolation_b_spline(base1, boat_history1)
    plt.show()

if __name__ == "__main__":
    simulation()
