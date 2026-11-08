"""Rebuild displayed table values and the forest plot from included CSVs."""
import argparse
import csv
import statistics
import math
from pathlib import Path

from release_support import ROOT, IndexedPath


def read(name):
    with IndexedPath(name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def tables():
    def three_significant(value):
        places = max(0, 2 - math.floor(math.log10(abs(value))))
        return f'{value:.{places}f}'
    effects = read('reports/compatibility_null_validation/controls_projection_power/C_effect_sizes_power.csv')
    diagnostic = read('results/contribution_step12/summary.csv')
    point = read('results/fair_comparison_step2/per_run.csv')
    probability = read('results/risk_context_step8/per_run.csv')
    manuscript = (ROOT / 'paper/manuscript.md').read_text(encoding='utf-8')
    existing = [block.splitlines() for block in manuscript.split('\n\n') if block.startswith('|') and '| FD' in block]
    assert len(existing) == 4
    # The IJPHM narrative presents Table 2 before Table 1; match by table identity.
    def table_number(lines):
        header = lines[0]
        return 1 if 'Group / outcome' in header else 2 if 'Raw incompatible' in header else 3 if 'Fit/test' in header else 4
    existing.sort(key=table_number)
    rows = [[], [], [], []]
    for subset in ['FD001', 'FD002', 'FD003', 'FD004']:
        for model in ['lstm', 'hybrid']:
            label = 'LSTM' if model == 'lstm' else 'Hybrid'
            group = [row for row in effects if row['scope'] == 'group' and row['subset'] == subset and row['architecture'] == model]
            assert len(group) == 2
            for outcome in ['median_squared_error', 'Brier']:
                row = next(item for item in group if item['outcome'] == outcome)
                cells = [f'{subset} {model} ' + ('median error' if outcome == 'median_squared_error' else 'Brier'),
                         row['fitting_engines'] + '/' + row['evaluation_engines'],
                         f"{float(row['coefficient']):.3g} [{float(row['ci_low']):.3g}, {float(row['ci_high']):.3g}]",
                         f"{float(row['mean_outcome_MSE']):.3g}",
                         f"{float(row['upper_CI_as_percent_of_mean']):.1f}%",
                         f"{float(row['MDE_80_power']):.3g} ({float(row['MDE_as_percent_of_mean']):.1f}%)"]
                rows[0].append(cells)
            raw = next(row for row in diagnostic if row['subset'] == subset and row['model'] == label and row['method'] == 'Raw')
            temp = next(row for row in diagnostic if row['subset'] == subset and row['model'] == label and row['method'] == 'Temp')
            rows[1].append([subset, label, str(int(float(raw['n_per_run']))),
                            f"{100*float(raw['fraction_mean']):.1f} ± {100*float(raw['fraction_sd']):.1f}",
                            f"{100*float(temp['fraction_mean']):.1f} ± {100*float(temp['fraction_sd']):.1f}",
                            f"{float(raw['mean_distance_mean']):.4f} ± {float(raw['mean_distance_sd']):.4f}"])
            runs = [row for row in point if row['subset'] == subset and row['model'] == model]
            assert len(runs) == 5
            point_cells = []
            for metric in ['RMSE', 'MAE']:
                values = [float(row[metric]) for row in runs]
                point_cells.append(three_significant(statistics.mean(values)) + ' ± ' + three_significant(statistics.stdev(values)))
            rows[2].append([subset, label, group[0]['fitting_engines'] + '/' + group[0]['evaluation_engines'], *point_cells, f"{float(raw['Brier_mean']):.5f}"])
            scores = []
            for method in ['Raw', 'Bayes', 'Temp', 'ShiftTemp']:
                values = [float(row['Brier']) for row in probability if row['study'] == 'EqualSearch' and row['subset'] == subset and row['model'] == label and row['method'] == method]
                assert len(values) == 5
                scores.append(f'{statistics.mean(values):.5f} ± {statistics.stdev(values):.5f}')
            rows[3].append([subset, label, group[0]['evaluation_engines'], *scores])
    output = ROOT / 'paper/generated_tables'
    output.mkdir(exist_ok=True)
    for index, data in enumerate(rows):
        lines = existing[index][:2] + ['| ' + ' | '.join(row) + ' |' for row in data]
        assert lines == existing[index], f'Table {index+1} differs from the unchanged manuscript table: ' + str([(a, b) for a, b in zip(lines, existing[index]) if a != b])
        (output / f'table_{index+1}.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('PASS: all 40 main-text data rows regenerated from CSVs at the displayed precision')


def figure():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows = [row for row in read('reports/compatibility_null_validation/calibrator_extension/A_all_scores.csv')
            if row['method'] == 'projection' and row['measure'] == 'Brier' and row['subset'] != 'pooled']
    assert len(rows) == 44
    fig, ax = plt.subplots(figsize=(8, 10.8))
    for index, row in enumerate(rows):
        value = float(row['difference_vs_raw'])
        low = float(row['difference_ci_low'])
        high = float(row['difference_ci_high'])
        ax.errorbar(value, index, xerr=[[value-low], [high-value]], fmt='o', color='#234f6b', ecolor='#71818d', markersize=3, capsize=2)
    ax.set_yticks(range(44), [f"{row['subset']} {row['family']}/{row['architecture']} (n={row['evaluation_engines']})" for row in rows], fontsize=7)
    ax.invert_yaxis()
    ax.axvline(0, color='black', linewidth=.8)
    ax.set_xlabel('Projection minus raw Brier (score units; negative favors projection)')
    ax.set_title('Exploratory comparison of 44 groups sharing 707 test engines')
    fig.tight_layout()
    output = ROOT / 'paper/figures'
    fig.savefig(output / 'projection_brier_44_groups_regenerated.png', dpi=220)
    fig.savefig(output / 'projection_brier_44_groups_regenerated.pdf')
    plt.close(fig)
    print('PASS: plotted 44 stored estimates and CIs without fitting or resampling')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['tables', 'figure'])
    args = parser.parse_args()
    {'tables': tables, 'figure': figure}[args.action]()
