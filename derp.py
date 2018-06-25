def relative_frequency_parties(df, parties):
    
    for i in parties:
        df['{}_p'.format(i)] = df['{}'.format(i)]/df['Gültige Stimmen']
    
    return df


def df_to_crs(df, from_epsg, to_epsg):
    try:
        assert type(from_epsg) == str and len(from_epsg) in range(4, 6)
        df.crs = {'init': 'epsg:{}'.format(from_epsg)}

        if type(to_epsg) == str and len(to_epsg) in range(4, 6):
            df = df.to_crs({'init': 'epsg:{}'.format(to_epsg)})
            return df
        else:
            raise ValueError
    except ValueError as v:
        print('Insert valid to_epsg code, see https://epsg.io')
    except AssertionError as a:
        print('Insert valid from_epsg code, see https://epsg.io')
