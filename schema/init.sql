DROP TABLE stock;
DROP TABLE crypto;
DROP TABLE future;
DROP TABLE index;
DROP TABLE meta;

CREATE TABLE meta (
    id SERIAL not null,
    m_type VARCHAR(20), --crypto|index|future|stock
    m_name VARCHAR(100),
    m_code VARCHAR(15),
    m_curr VARCHAR(10),
    m_url VARCHAR(200),
    m_open TIMESTAMP null,
    m_close TIMESTAMP null,
    constraint PK_meta primary key (id)
);

CREATE TABLE stock (
    id SERIAL not null,
    meta_id INTEGER not null REFERENCES meta(id),
    price FLOAT,
    created_at TIMESTAMP,
    constraint PK_stock primary key (id)
);

CREATE TABLE index (
    id SERIAL not null,
    meta_id INTEGER not null REFERENCES meta(id),
    price FLOAT,
    created_at TIMESTAMP,
    constraint PK_index primary key (id)
);

CREATE TABLE future (
    id SERIAL not null,
    meta_id INTEGER not null REFERENCES meta(id),
    price FLOAT,
    created_at TIMESTAMP,
    constraint PK_future primary key (id)
);

CREATE TABLE crypto (
    id SERIAL not null,
    meta_id INTEGER not null REFERENCES meta(id),
    price FLOAT,
    created_at TIMESTAMP,
    constraint PK_crypto primary key (id)
);
--STOCKS META
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Apple Inc.', 'stock', 'AAPL', 'USD', 'https://www.marketwatch.com/investing/stock/aapl');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Lexicon Pharmaceuticals Inc.', 'stock', 'LXRX', 'USD', 'https://www.marketwatch.com/investing/stock/lxrx');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Alphabet Inc. Cl A', 'stock', 'GOOGL', 'USD', 'https://www.marketwatch.com/investing/stock/googl');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Alphabet Inc. Cl C', 'stock', 'GOOG', 'USD', 'https://www.marketwatch.com/investing/stock/goog');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Plug Power Inc.', 'stock', 'PLUG', 'USD', 'https://www.marketwatch.com/investing/stock/plug');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Exxon Mobil Corp.', 'stock', 'XOM', 'USD', 'https://www.marketwatch.com/investing/stock/xom');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Visa Inc. Cl A', 'stock', 'V', 'USD', 'https://www.marketwatch.com/investing/stock/v');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Procter & Gamble Co.', 'stock', 'PG', 'USD', 'https://www.marketwatch.com/investing/stock/pg');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('JPMorgan Chase & Co.', 'stock', 'JPM', 'USD', 'https://www.marketwatch.com/investing/stock/jpm');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('XPeng Inc. ADR', 'stock', 'XPEV', 'USD', 'https://www.marketwatch.com/investing/stock/xpev');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Meta Platforms Inc.', 'stock', 'META', 'USD', 'https://www.marketwatch.com/investing/stock/meta');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Microsoft Corp.', 'stock', 'MSFT', 'USD', 'https://www.marketwatch.com/investing/stock/msft');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Amazon.com Inc.', 'stock', 'AMZN', 'USD', 'https://www.marketwatch.com/investing/stock/amzn');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Tesla Inc.', 'stock', 'TSLA', 'USD', 'https://www.marketwatch.com/investing/stock/tsla');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Berkshire Hathaway Inc. Cl B.', 'stock', 'BRK.B', 'USD', 'https://www.marketwatch.com/investing/stock/brk.b');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('UnitedHealth Group Inc.', 'stock', 'UNH', 'USD', 'https://www.marketwatch.com/investing/stock/unh');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Johnson & Johnson', 'stock', 'JNJ', 'USD', 'https://www.marketwatch.com/investing/stock/jnj');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('NVIDIA Corp.', 'stock', 'NVDA', 'USD', 'https://www.marketwatch.com/investing/stock/nvda');

--INDEX META
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('DAX', 'index', 'DAX', 'INDEX', 'https://www.marketwatch.com/investing/index/dax?countrycode=dx');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Dow Jones Industrial Average', 'index', 'DJIA', 'INDEX', 'https://www.marketwatch.com/investing/index/djia');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('FTSE ALL-WORLD', 'index', 'FTSE-AWORLD', 'INDEX', 'https://markets.businessinsider.com/index/ftse-aworld');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('NASDAQ Composite Index', 'index', 'COMP', 'INDEX', 'https://www.marketwatch.com/investing/index/comp');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('FTSE 100 Index', 'index', 'UKX', 'INDEX', 'https://www.marketwatch.com/investing/index/ukx?countryCode=UK');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Nifty 50 Index', 'index', 'NIFTY50', 'INDEX', 'https://www.marketwatch.com/investing/index/nifty50');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('NIKKEI 225 Index', 'index', 'NIK', 'INDEX', 'https://www.marketwatch.com/investing/index/nik');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('S&P 500 Index', 'index', 'SPX', 'INDEX', 'https://www.marketwatch.com/investing/index/spx');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('MOEX Russia Index', 'index', 'MOEX', 'INDEX', 'https://www.cnbc.com/quotes/.IMOEX');

--FUTURE META
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('E-Mini S&P 500 Future Continuous Contract', 'future', 'SP500', 'USD', 'https://www.marketwatch.com/investing/future/sp%20500%20futures');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('FTSE 100 Index Continuous Contract', 'future', 'FTSE100', 'GBP', 'https://www.marketwatch.com/investing/future/z00');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('DAX Index Continuous Contract', 'future', 'DAX', 'EUR', 'https://www.marketwatch.com/investing/future/dax00');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Gold Continuous Contract', 'future', 'GOLD', 'USD', 'https://www.marketwatch.com/investing/future/gold');

--CRYPTO META
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Dogecoin', 'crypto', 'DOGE', 'USD', 'https://www.marketwatch.com/investing/cryptocurrency/dogeusd');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Ethereum', 'crypto', 'ETH', 'USD', 'https://www.marketwatch.com/investing/cryptocurrency/ethusd');
INSERT INTO meta (m_name, m_type, m_code, m_curr, m_url) VALUES ('Bitcoin', 'crypto', 'BTC', 'USD', 'https://www.marketwatch.com/investing/cryptocurrency/btcusd');