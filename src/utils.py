import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


def hist_box_plot(data, target=None, title='', xlabel='', ylabel='', figx=9, figy=7):
    plt.figure(figsize=(figx, figy))

    # Histogram
    plt.subplot(1, 2, 1)
    if target is not None:
        unique_labels = np.unique(target)
        for label in unique_labels:
            plt.hist(data[target == label], alpha=0.5, label=f'Target {label}')
        plt.legend()
    else:
        plt.hist(data)
    plt.title(f'{title} - Histogram')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Boxplot
    plt.subplot(1, 2, 2)
    if target is not None:
        sns.boxplot(x=target, y=data)
    else:
        sns.boxplot(x=data)
    plt.title(f'{title} - Boxplot')
    plt.xlabel('Target' if target is not None else xlabel)
    plt.ylabel(ylabel)

    plt.tight_layout()
    plt.show()


def bar_plot(data, target=None, title='', xlabel='', ylabel='', proportional=False,
             figx=9, figy=7, feature='x', horizontal=False):
    plt.figure(figsize=(figx, figy))

    if target is not None:
        temp_df = pd.DataFrame({'feature': data, 'target': target})

        if proportional:
            ctab = pd.crosstab(temp_df['feature'],
                               temp_df['target'], normalize='index')
            ax = ctab.plot(kind='barh' if horizontal else 'bar', stacked=True,
                           colormap='coolwarm', width=0.8)
            plt.title(title)
            plt.xlabel(xlabel if not horizontal else 'Proportion')
            plt.ylabel(ylabel if not horizontal else xlabel)
            plt.xticks(rotation=30 if not horizontal else 0)

            # Label proporsi di bar
            for i, cat in enumerate(ctab.index):
                bottom = 0
                for j, cls in enumerate(ctab.columns):
                    pct = ctab.loc[cat, cls]
                    if pct > 0.01:
                        if horizontal:
                            ax.text(
                                x=bottom + pct / 2,
                                y=i,
                                s=f"{pct*100:.1f}%",
                                ha='center',
                                va='center',
                                fontsize=9,
                                color='white' if pct > 0.25 else 'black'
                            )
                        else:
                            ax.text(
                                x=i,
                                y=bottom + pct / 2,
                                s=f"{pct*100:.1f}%",
                                ha='center',
                                va='center',
                                fontsize=9,
                                color='white' if pct > 0.25 else 'black'
                            )
                    bottom += pct

        else:
            if horizontal:
                sns.countplot(y='feature', hue='target', data=temp_df)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
            else:
                sns.countplot(x='feature', hue='target', data=temp_df)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)

            plt.title(title)
            plt.xticks(rotation=30 if not horizontal else 0)
            plt.tight_layout()
            plt.show()
            return

    else:
        counts = data.value_counts()
        if horizontal:
            plt.barh(counts.index, counts.values)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
        else:
            plt.bar(counts.index, counts.values)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

    plt.title(title)
    plt.xticks(rotation=30 if not horizontal else 0)
    plt.tight_layout()
    plt.show()


def heatmap(data, title=""):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.heatmap(data, annot=True, cmap='Blues', fmt='.2f')
    plt.title(title)
    plt.tight_layout()
    plt.show()


def cramers_v(x, y):
    import pandas as pd
    import numpy as np
    from scipy.stats import chi2_contingency

    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape

    phi2_corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    r_corr = r - ((r - 1) ** 2) / (n - 1)
    k_corr = k - ((k - 1) ** 2) / (n - 1)

    return np.sqrt(phi2_corr / min((k_corr - 1), (r_corr - 1)))


def cramers_v_matrix(df):
    import pandas as pd
    cat_cols = df.select_dtypes(include='object').columns
    result = pd.DataFrame(index=cat_cols, columns=cat_cols)

    for col1 in cat_cols:
        for col2 in cat_cols:
            result.loc[col1, col2] = cramers_v(df[col1], df[col2])

    return result.astype(float)


def violin_plot(x, y, data, title='', x_label='', y_label='', figx=9, figy=7):
    plt.figure(figsize=(figx, figy))
    sns.violinplot(x=x, y=y, data=data)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def scatter_plot(x, y, title='', xlabel='', ylabel='', figx=9, figy=7):
    plt.figure(figsize=(figx, figy))
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()
