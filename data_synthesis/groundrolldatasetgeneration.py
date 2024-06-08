import os
import numpy as np
import matplotlib.pyplot as plt

def ground_roll_syn(num_traces=100,
                    num_time_samples=1000,
                    time_shift=50,
                    freq_low=5,
                    freq_high=20,
                    dx=5,
                    dt=0.002,
                    velocity=100,
                    distance_degradation=0.92,
                    win_scale=4,
                    duration_ratio=0.04,
                    save_path='./syn_data/sample_groundroll.npy',
                    verbose=False):
    """
    args:
        num_traces: number of seismic traces (single side w.r.t source point)
        num_time_samples: number of samples in time axis
        time_shift: offset to the top
        freq_low: the lower frequency of the chirp signal to simulate dispersity
        freq_high: the higher frequency of the chirp signal to simulate dispersity
        dx: space sample interval (unit: m)
        dy: time sample interval (unit: s)
        velocity: ground-roll velocity (unit: m/s)
        distance_degradation: amplitude degradation ratio w.r.t distance
        win_scale: controls the smooth edge of window, should be larger than (or equal to) 2, the larger the shearer
        duration_ratio: controls the sampling of chirp of ground-roll in each trace
        save_path: synthetic data save path, if parent folder not exist, it will be created
        verbose: if True, displays the generated image
    """
    dp = dx / (velocity * dt)  # reciprocal of radial velocity
    gr_data = np.zeros((num_time_samples, num_traces))

    for trace_idx in range(num_traces):
        # step 1. generate chirp signal
        T = 1 + trace_idx * duration_ratio
        bandwidth = freq_high - freq_low
        t = np.arange(0, T, dt) / (2 * T)
        Ft = (freq_low + bandwidth * t)
        chirp_signal = np.sin(2 * np.pi * Ft * t)

        # step 2. generate window
        window = np.ones(len(t))
        n_edge = int(np.round(np.pi / (2 * dt * win_scale)))
        # make sure the window is sin-edge + plateau + sin-edge (symm) format
        if n_edge >= len(t) / 2:
            print(f"Skipping trace_idx={trace_idx} due to invalid n_edge: {n_edge} >= {len(t) / 2}")
            continue
        t1 = np.arange(0, n_edge * dt, dt)
        edge = np.sin(t1 * win_scale)
        window[:n_edge] = edge
        window[-n_edge:] = edge[::-1]

        # step 3. gen simulated ground-roll
        gr_w = window * chirp_signal
        t_offset = int(np.round(trace_idx * dp) + time_shift)
        cur_deg = distance_degradation ** trace_idx

        if t_offset > num_time_samples:
            break
        elif t_offset + len(t) > num_time_samples:
            cutoff_N = num_time_samples - t_offset
            gr_data[t_offset:, trace_idx] = gr_w[:cutoff_N] * cur_deg
        else:
            gr_data[t_offset: t_offset + len(t), trace_idx] = gr_w[:len(t)] * cur_deg

    if verbose:
        plt.imshow(gr_data, aspect='auto')
        plt.show()
    
    # save result
    dir_name = os.path.dirname(save_path)
    os.makedirs(dir_name, exist_ok=True)
    np.save(save_path, gr_data)

if __name__ == "__main__":
    # Define ranges for parameters
    num_traces_range = [50, 100, 150]
    num_time_samples_range = [500, 1000, 1500]
    time_shift_range = [30, 50, 70]
    freq_low_range = [3, 5, 7]
    freq_high_range = [15, 20, 25]
    dx_range = [3, 5, 7]
    dt_range = [0.001, 0.002, 0.003]
    velocity_range = [80, 100, 120]
    distance_degradation_range = [0.9, 0.92, 0.94]
    win_scale_range = [2, 4, 6]
    duration_ratio_range = [0.02, 0.04, 0.06]

    # Counter to keep track of number of images generated
    counter = 0

    # Loop over all combinations of parameter ranges
    for num_traces in num_traces_range:
        for num_time_samples in num_time_samples_range:
            for time_shift in time_shift_range:
                for freq_low in freq_low_range:
                    for freq_high in freq_high_range:
                        for dx in dx_range:
                            for dt in dt_range:
                                for velocity in velocity_range:
                                    for distance_degradation in distance_degradation_range:
                                        for win_scale in win_scale_range:
                                            for duration_ratio in duration_ratio_range:
                                                # Ensure condition n_edge < len(t)/2
                                                T = 1 + num_traces * duration_ratio
                                                t = np.arange(0, T, dt) / (2 * T)
                                                n_edge = int(np.round(np.pi / (2 * dt * win_scale)))
                                                if n_edge < len(t) / 2:
                                                    # Generate and save image
                                                    save_path = f'./syn_data/sample_groundroll_{counter}.npy'
                                                    ground_roll_syn(num_traces=num_traces,
                                                                    num_time_samples=num_time_samples,
                                                                    time_shift=time_shift,
                                                                    freq_low=freq_low,
                                                                    freq_high=freq_high,
                                                                    dx=dx,
                                                                    dt=dt,
                                                                    velocity=velocity,
                                                                    distance_degradation=distance_degradation,
                                                                    win_scale=win_scale,
                                                                    duration_ratio=duration_ratio,
                                                                    save_path=save_path,
                                                                    verbose=False)
                                                    counter += 1
                                                    if counter >= 50000:
                                                        break
                                                else:
                                                    print(f"Skipping parameters due to invalid n_edge: {n_edge} >= {len(t) / 2}")
                                            if counter >= 50000:
                                                break
                                        if counter >= 50000:
                                            break
                                    if counter >= 50000:
                                        break
                                if counter >= 50000:
                                    break
                            if counter >= 50000:
                                break
                        if counter >= 50000:
                            break
                    if counter >= 50000:
                        break
                if counter >= 50000:
                    break
            if counter >= 50000:
                break
        if counter >= 50000:
            break

    print(f"Generated {counter} images.")
