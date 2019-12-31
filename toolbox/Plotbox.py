import matplotlib.pyplot as plt
import mpld3
import numpy as np
import datetime as dt
import collections
import json
from dataset.dataset_example import data as data_

class Plotbox():

    def __init__(self):
        self.data = data_
        self.legend_labels = self.dataset_names()

    def dataset_names(self):
        return [d['legend_label'] for d in self.data]

    def normalize_dataset(self, data):
        """
            normalizing each item in dataset/list to be in range from 0 to 100
        """
        normalized_data = data

        values = list(normalized_data.values())
        min_item, max_item = min(values), max(values)
        denominator = max_item - min_item

        for key in normalized_data.keys():
            normalized_data[key] = ((normalized_data[key] - min_item) / denominator) * 100

        return normalized_data

    def get_n_random_colors(self, n):
        """
            Generating list of lists, each nested list is one color. Each color have random numbers
            for R, G, B values
        """

        colors = []

        for i in range(n):
            color2 = np.random.rand(3, )

            color1 = color2.__copy__()
            color1[1] = color1[1] + 0.2 if color1[1] + 0.2 < 1 else color1[1] + 0.2 - 1

            colors.append((color1, color2))

        return colors

    def line_charts(self, datasets, legend, gridlines=False, all=False):
        colors = self.get_n_random_colors(len(datasets))

        if all:
            fig, ax = plt.subplots(figsize=(15, 6))

        plots = []
        for color, d, l in zip(colors, datasets, legend):
            color = np.random.rand(3, )

            if not all:
                fig, ax = plt.subplots(figsize=(15, 6))

            d = collections.OrderedDict(sorted(d.items()))

            new_d = {}
            for key in d.keys():
                if d[key] > 0:
                    new_d[key] = d[key]

            x = list(new_d.keys())
            y = list(new_d.values())

            plots.append(
                plt.plot(x, y, marker='o', markerfacecolor=color, markersize=8, color=color, linewidth=2, label=l)
            )
            plt.xticks(list(d.keys()), rotation=30, ha="right", fontsize=7)

            if gridlines:
                plt.grid(color='blue', alpha=0.3)
                ax.xaxis.grid()

            if not all:
                plt.legend(loc='upper right')
                plt.show()

                mpld3.save_html(fig, 'output/dataset_{}.html'.format(l))

        fig.tight_layout()

        if all:
            plt.legend(loc='upper right')
            plt.show()

            mpld3.save_html(fig, 'output/all.html')

    def json_to_list(self, json_list, key_date, key_num):
        date_num = {}

        for item in json_list:
            if not isinstance(item[key_date], dt.date) or not isinstance(item[key_date], dt.datetime):
                item[key_date] = dt.datetime.strptime(item[key_date], '%Y-%m-%d')

            date_num[item[key_date]] = item[key_num]

        date_num = self.fill_missing_dates(date_num)

        return date_num

    def fill_missing_dates(self, d):
        min_date = min(d.keys())
        max_date = max(d.keys())

        delta = (max_date - min_date).days

        for i in range(delta):
            if (min_date + dt.timedelta(i)) not in d.keys():
                d[min_date + dt.timedelta(i)] = 0

        return d

    def transform_data(self):
        transformed_data = []

        for d in self.data:
            date_val = {}

            for item in d['dataset']:
                date, val = None, None

                for k in item.keys():
                    try:
                        item[k] = dt.datetime.strptime(item[k], '%Y-%m-%d')
                    except:
                        item[k] = item[k]

                    if isinstance(item[k], dt.datetime) or isinstance(item[k], dt.date):
                        date = item[k]

                    if isinstance(item[k], int) or isinstance(item[k], float):
                        val = item[k]

                    if date is not None and val is not None:
                        break

                date_val[date] = val

            transformed_data.append({
                d['legend_label']: self.fill_missing_dates(date_val)
            })

        return transformed_data

    def save_output_data(self):
        output = self.transform_data()

        new_data = {}
        for item in output:
            k = list(item.keys())[0]

            vals = {}
            for key in item[k].keys():
                vals[dt.datetime.strftime(key, '%Y-%m-%d')] = item[k][key]

            new_data[k] = vals
        output = new_data

        self.line_charts(list(output.values()), list(output.keys()), True)

        output = json.dumps(output)
        with open('./output/output.json', 'w') as outfile:
            json.dump(output, outfile)


if __name__ == '__main__':
    p = Plotbox()

    p.save_output_data()
