# Revisión profunda de candidatos BRI LATAM — Script 19

**Total revisados:** 60  
**CONFIRMED:** 6 | **LIKELY:** 2 | **WEAK:** 0 | **NOISE:** 52

## Metodología
- Se descargan los artículos de las URLs del dataset curado
- Se extrae: empresa china mencionada, keywords de disrupción, keywords BRI
- Nivel de confirmación = función de: empresa_mencionada × disrupción × contexto_BRI × volumen_GKG
- **CONFIRMED**: empresa + ≥2 disrupciones + contexto BRI claro
- **LIKELY**: empresa + disrupción O contexto BRI claro
- **WEAK**: señal débil (solo URL keyword, artículo no accesible, etc.)
- **NOISE**: URL muerta o sin relevancia

## ✅ CONFIRMED (6 señales)

### Venezuela × SOE_OIL × 2019
- **Mecanismo**: confirmed_presence
- **Tono**: -4.04 | N artículos GKG: 230
- **Empresa mencionada**: PetroChina
- **Keywords disrupción**: cancel, suspend, block, sanction, pull out
- **Keywords BRI**: bri
- **Proyecto (heurística)**: port Options Unlocked Watch Now Spor
- **Título artículo**: Will PetroChina Pull Out of Venezuela Amid US Sanctions?
- **URL**: [https://finance.yahoo.com/news/petrochina-pull-venezuela-amid-us-12501](https://finance.yahoo.com/news/petrochina-pull-venezuela-amid-us-125012728.html)
- **Fuente GDELT**: GKG

### Ecuador × SOE_OIL × 2023
- **Mecanismo**: confirmed_presence
- **Tono**: -6.21 | N artículos GKG: 14
- **Empresa mencionada**: PetroChina
- **Keywords disrupción**: suspend, renegotiat
- **Keywords BRI**: bri
- **Proyecto (heurística)**: —
- **Título artículo**: Ecuador’s anti-corruption presidential candidate was shot dead
- **URL**: [https://qz.com/ecuador-fernando-villavicencio-corruption-assassination](https://qz.com/ecuador-fernando-villavicencio-corruption-assassination-1850723921)
- **Fuente GDELT**: GKG

### Colombia × SOE_OIL × 2023
- **Mecanismo**: confirmed_presence
- **Tono**: -6.11 | N artículos GKG: 14
- **Empresa mencionada**: PetroChina
- **Keywords disrupción**: suspend, renegotiat
- **Keywords BRI**: bri
- **Proyecto (heurística)**: —
- **Título artículo**: Ecuador’s anti-corruption presidential candidate was shot dead
- **URL**: [https://qz.com/ecuador-fernando-villavicencio-corruption-assassination](https://qz.com/ecuador-fernando-villavicencio-corruption-assassination-1850723921)
- **Fuente GDELT**: GKG

### Chile × SOE_OIL × 2020
- **Mecanismo**: confirmed_presence
- **Tono**: -4.41 | N artículos GKG: 37
- **Empresa mencionada**: Sinopec, CNOOC
- **Keywords disrupción**: cancel, suspend, suspender
- **Keywords BRI**: —
- **Proyecto (heurística)**: —
- **Título artículo**: China agrava caos com força maior em contratos de commodities - 07/02/2020 - UOL Economia
- **URL**: [https://economia.uol.com.br/noticias/bloomberg/2020/02/07/china-agrava](https://economia.uol.com.br/noticias/bloomberg/2020/02/07/china-agrava-caos-com-forca-maior-em-contratos-de-commodities.htm)
- **Fuente GDELT**: GKG

### Brasil × SOE_OIL × 2023
- **Mecanismo**: confirmed_presence
- **Tono**: -4.37 | N artículos GKG: 35
- **Empresa mencionada**: PetroChina
- **Keywords disrupción**: suspend, renegotiat
- **Keywords BRI**: bri
- **Proyecto (heurística)**: —
- **Título artículo**: Ecuador’s anti-corruption presidential candidate was shot dead
- **URL**: [https://qz.com/ecuador-fernando-villavicencio-corruption-assassination](https://qz.com/ecuador-fernando-villavicencio-corruption-assassination-1850723921)
- **Fuente GDELT**: GKG

### México × SOE_OIL × 2023
- **Mecanismo**: confirmed_presence
- **Tono**: -5.31 | N artículos GKG: 13
- **Empresa mencionada**: PetroChina
- **Keywords disrupción**: suspend, renegotiat
- **Keywords BRI**: bri
- **Proyecto (heurística)**: —
- **Título artículo**: Ecuador’s anti-corruption presidential candidate was shot dead
- **URL**: [https://qz.com/ecuador-fernando-villavicencio-corruption-assassination](https://qz.com/ecuador-fernando-villavicencio-corruption-assassination-1850723921)
- **Fuente GDELT**: GKG

## 🟡 LIKELY (2 señales)

### Cuba × SOE_MARITIME × 2019
- **Mecanismo**: confirmed_presence
- **Tono**: -4.67 | N artículos GKG: 40
- **Empresa mencionada**: Cosco
- **Keywords disrupción**: paralizado
- **Keywords BRI**: —
- **Proyecto (heurística)**: —
- **Título artículo**: Petroleros “desaparecen” ante Venezuela para evadir las sanciones de EE.UU. | MUNDO | GESTIÓN
- **URL**: [https://gestion.pe/mundo/internacional/petroleros-desaparecen-ante-ven](https://gestion.pe/mundo/internacional/petroleros-desaparecen-ante-venezuela-para-evadir-las-sanciones-de-eeuu-noticia/)
- **Fuente GDELT**: GKG

### Venezuela × SOE_OIL × 2024
- **Mecanismo**: confirmed_presence
- **Tono**: -4.01 | N artículos GKG: 36
- **Empresa mencionada**: Petrochina
- **Keywords disrupción**: suspend
- **Keywords BRI**: —
- **Proyecto (heurística)**: —
- **Título artículo**: Uma região sob domínio do narcotráfico
- **URL**: [https://www.correiodopovo.com.br/colunistas/jurandir-soares/uma-regi%C](https://www.correiodopovo.com.br/colunistas/jurandir-soares/uma-regi%C3%A3o-sob-dom%C3%ADnio-do-narcotr%C3%A1fico-1.1457544)
- **Fuente GDELT**: GKG

## ⬜ NOISE — URLs muertas o sin relevancia

- Guatemala 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Costa Rica 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Nicaragua 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Bolivia 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Honduras 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Haití 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Cuba 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Ecuador 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Argentina 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Panamá 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Venezuela 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Chile 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Brasil 2021 confirmed_presence — error: sin evidencia | http://www.hinews.cn/news/system/2021/04/09/032536464.shtml
- Chile 2022 confirmed_presence — error: sin evidencia | http://sc.sina.com.cn/news/b/2022-01-31/detail-ikyakumy35292
- Venezuela 2018 confirmed_presence — error: HTTP 404 | http://news.cnfol.com/chanyejingji/20180810/26744959.shtml
- Ecuador 2021 confirmed_presence — error: HTTP 403 | https://www.westport-news.com/news/article/Great-Wall-of-Lig
- Venezuela 2019 confirmed_presence — error: sin evidencia | http://newsabah.com/newspaper/196066
- Chile 2019 confirmed_presence — error: sin evidencia | http://hk.eastmoney.com/a/201901231032796874.html
- Brasil 2017 confirmed_presence — error: sin evidencia | http://world.qianlong.com/2017/1127/2203949.shtml
- México 2017 confirmed_presence — error: sin evidencia | http://china.qianlong.com/2017/0606/1744069.shtml
- Brasil 2020 confirmed_presence — error: HTTPConnectionPool(host='origin-businesstoday.intoday.in', port=80): Max retries | http://origin-businesstoday.intoday.in/current/economy-polit
- Argentina 2021 confirmed_presence — error: HTTP 403 | https://www.westport-news.com/news/article/Great-Wall-of-Lig
- México 2021 confirmed_presence — error: HTTP 403 | https://www.westport-news.com/news/article/Great-Wall-of-Lig
- Chile 2021 confirmed_presence — error: timeout | https://www.washingtonpost.com/business/great-wall-of-lights
- Venezuela 2017 confirmed_presence — error: HTTP 403 | http://dailytimes.com.pk/business/23-Jul-17/us-weighs-financ
- Brasil 2019 confirmed_presence — error: sin evidencia | http://www.sohu.com/a/342100104_260616
- Brasil 2020 confirmed_presence — error: sin evidencia | https://www.yicai.com/news/100626711.html
- Chile 2020 confirmed_presence — error: sin evidencia | https://finance.sina.com.cn/roll/2020-08-10/doc-iivhuipn7753
- Ecuador 2017 confirmed_presence — error: sin evidencia | http://www.xinhuanet.com/world/2017-12/26/c_1122169904.htm
- Venezuela 2020 confirmed_presence — error: sin evidencia | http://futures.eastmoney.com/a/202002071375403522.html
- Brasil 2018 confirmed_presence — error: sin evidencia | http://www.cfi.net.cn/p20180524001932.html
- Venezuela 2017 confirmed_presence — error: sin evidencia | https://sputnik-georgia.ru/incidents/20170210/234826809/Figu
- Colombia 2017 confirmed_presence — error: sin evidencia | http://www.xinhuanet.com/world/2017-12/26/c_1122169904.htm
- Venezuela 2022 confirmed_presence — error: sin evidencia | https://blog.wenxuecity.com/myblog/72378/202207/4990.html
- Bolivia 2019 confirmed_presence — error: HTTP 403 | https://elpotosi.net/nacional/20190422_denuncian-a-empresa-c
- Bolivia 2023 confirmed_presence — error: HTTP 404 | https://www.iraqicp.com/index.php/sections/news/63607-2023-0
- Chile 2019 confirmed_presence — error: sin evidencia | https://finance.sina.com.cn/stock/relnews/hk/2019-10-22/doc-
- México 2019 confirmed_presence — error: HTTP 404 | http://news.stcn.com/2019/0603/15157126.shtml
- México 2021 confirmed_presence — error: sin evidencia | https://www.chinatimes.com/newspapers/20210318000159-260203
- Chile 2019 confirmed_presence — error: sin evidencia | http://stock.eastmoney.com/a/201905291137258059.html
- México 2020 confirmed_presence — error: sin evidencia | http://finance.eastmoney.com/a/202004221463625230.html
- Brasil 2018 confirmed_presence — error: HTTP 404 | https://www.hellenicshippingnews.com/protection-vessels-inte
- Venezuela 2023 confirmed_presence — error: sin evidencia | https://mzamin.com/news.php?news=78844
- México 2018 confirmed_presence — error: HTTP 404 | https://udn.com/news/story/7251/3238080
- Bolivia 2017 confirmed_presence — error: sin evidencia | http://www.paginasiete.bo/economia/2017/9/21/trabajadores-em
- Brasil 2022 confirmed_presence — error: sin evidencia | https://www.voacantonese.com/a/china-may-oil-imports-from-ru
- México 2020 confirmed_presence — error: sin evidencia | http://stock.finance.sina.com.cn/stock/go.php/vReport_Show/k
- Brasil 2019 confirmed_presence — error: sin evidencia | https://opinion.udn.com/opinion/story/120626/4071710
- Chile 2017 confirmed_presence — error: sin evidencia | http://mp.3g.cnfol.com/pc/article/1010143
- Brasil 2020 confirmed_presence — error: sin evidencia | http://stock.jrj.com.cn/2020/06/08084629868736.shtml
- México 2022 confirmed_presence — error: sin evidencia | https://www.tayyar.org/News/World/513607/_guid=513607
- Argentina 2020 confirmed_presence — error: sin evidencia | https://www.yicai.com/news/100626711.html

## Próximo paso sugerido
- Revisar manualmente los CONFIRMED y LIKELY (abrir URL, verificar proyecto)
- Cruzar contra AidData TUFF 3.0 (descargar de aiddata.org) por país+año+SOE
- Los CONFIRMED nuevos → añadir a tabla de casos conocidos en la tesis
