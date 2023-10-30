def train(front_bl, fechas_train, fechas_test):

    dct_dow = {
        0: 'lunes',
        1: 'martes',
        2: 'miércoles',
        3: 'jueves',
        4: 'viernes',
        5: 'sábado',
        6: 'domingo',
    }

    def datetime_attributes(df):
        df['hour'] = df.index.hour
        df['day'] = df.index.day
        df['dow'] = df.index.dayofweek.map(dct_dow)
        df['cont_dow'] = (24 * df.index.dayofweek + df.index.hour) / 24
        df['week'] = df.index.isocalendar().week
        df['month'] = df.index.month
        df['year'] = df.index.year
        return df

    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    import pickle

    front_bl = datetime_attributes(front_bl)

    X = front_bl[['hour', 'cont_dow']]
    y = front_bl['value']


    X_train = X.loc[fechas_train[0]:fechas_train[1]	]
    X_test = X.loc[fechas_test[0]:fechas_test[1]]
    y_train = y.loc[fechas_train[0]:fechas_train[1]]
    y_test = y.loc[fechas_test[0]:fechas_test[1]]

    model = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(2),
        LinearRegression()
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    MSE = mean_squared_error(y_test, y_pred)

    filename = 'model/finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

    return model, MSE
