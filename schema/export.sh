#!/bin/bash

from='2022-09-01'
to='2022-10-01'
table='future'
target="/home/stock_sniffer/exports/${table}_${to}.csv"

cmd="SELECT m.m_name, m.id as name_id, m.m_code, m.m_type, m.m_curr, e.price, e.created_at FROM meta as m, ${table} as e where m.id=e.meta_id and e.created_at>'${from}' and e.created_at<'${to}' order by e.created_at ASC"
echo $cmd
cmd_main="\COPY (${cmd}) TO '${target}' WITH DELIMITER '\`' CSV HEADER;"
echo $cmd_main
# psql -h localhost -U postgres -d stock_sniffer -c "$cmd_main"
psql -c "$cmd_main"