DROP TABLE meta_init;
DROP TABLE cryptos;
DROP TABLE futures;
DROP TABLE stocks;
DROP TABLE indexes;


CREATE TABLE meta_init (
    id SERIAL not null,
    name VARCHAR(50) not null,
    type VARCHAR(10) not null, -- crypto, index, stock, future
    currency VARCHAR(10),
    source VARCHAR(200) null,
    trade_open TIMESTAMP null,
    trade_close TIMESTAMP null,

    constraint PK_meta_init primary key (id)
);

CREATE TABLE cryptos (
    name_id INTEGER not null,
    created_at TIMESTAMP not null,
    price FLOAT(7),
    PRIMARY KEY(name_id, created_at)
);

CREATE TABLE indexes (
    name_id INTEGER not null,
    created_at TIMESTAMP not null,
    price FLOAT(7) not null,
    PRIMARY KEY(name_id, created_at)
);

CREATE TABLE stocks (
    name_id INTEGER not null,
    created_at TIMESTAMP not null,
    price FLOAT(7) not null,
    PRIMARY KEY(name_id, created_at)
);

CREATE TABLE futures (
    name_id INTEGER not null,
    created_at TIMESTAMP not null,
    price FLOAT(7) not null,
    PRIMARY KEY(name_id, created_at)
);

INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('btc','crypto','https://www.marketwatch.com/investing/cryptocurrency/btcusd', 'usd', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('eth','crypto','https://www.marketwatch.com/investing/cryptocurrency/etheur', 'eur', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('doge','crypto','https://www.marketwatch.com/investing/cryptocurrency/dogeusd', 'usd', null, null);

INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('Dow Jones Industrial Average','index','https://www.marketwatch.com/investing/index/djia', null, null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('S&P 500 Index','index','https://www.marketwatch.com/investing/index/spx', null, null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('NASDAQ Composite Index','index','https://www.marketwatch.com/investing/index/comp', null, null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('DAX','index','https://www.marketwatch.com/investing/index/dax?countrycode=dx', null, null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('NIKKEI 225 Index','index','https://www.marketwatch.com/investing/index/nik?countryCode=JP', null, null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('Nifty 50 Index','index','https://www.marketwatch.com/investing/index/nifty50?countryCode=IN', null, null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('FTSE 100 Index','index','https://www.marketwatch.com/investing/index/ukx?countrycode=uk', null, null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('FTSE ALL-WORLD','index','https://markets.businessinsider.com/index/ftse-aworld', null, null, null);

INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('E-Mini S&P 500 Future Continuous Contract','future','https://www.marketwatch.com/investing/future/es00', 'usd', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('FTSE 100 Index Continuous Contract','future','https://www.marketwatch.com/investing/future/z00?countrycode=UK', 'gbp', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('DAX Index Continuous Contract','future','https://www.marketwatch.com/investing/future/dax00?countryCode=DE&iso=XEUR', 'eur', null, null);

INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('Lexicon Pharmaceuticals Inc.','stock','https://www.marketwatch.com/investing/stock/lxrx', 'usd', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('Apple Inc.','stock','https://www.marketwatch.com/investing/stock/aapl', 'usd', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('Alphabet Inc. Cl A','stock','https://www.marketwatch.com/investing/stock/googl', 'usd', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('Plug Power Inc.','stock','https://www.marketwatch.com/investing/stock/plug', 'usd', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('XPeng Inc. ADR','stock','https://www.marketwatch.com/investing/stock/xpev', 'usd', null, null);
INSERT INTO meta_init (name, type, source, currency, trade_open, trade_close) VALUES ('Facebook Inc. Cl A','stock','https://www.marketwatch.com/investing/stock/fb', 'usd', null, null);

