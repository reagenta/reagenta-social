V = '/home/claude/work/voice/'
SPECS = {}

SPECS['ecm'] = dict(
    id='ecm', voice=V + 'ecm.mp3', asr=V + 'ecm.json',
    foot=['Fonti: CNFC, delibera 1 del 5/3/2026; FNOMCeO, com. n. 42/2026; Quotidiano Sanità',
          'Esoneri e riduzioni variano caso per caso · verifica sul portale Cogeaps'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='ECM · TRIENNIO 2026-2028'),
            dict(t='gap', h=40),
            dict(t='title', text='Quanti crediti|*ECM*|ti servono|davvero?', size=118)]),
        dict(at='per il triennio', items=[
            dict(t='chip', text='OBBLIGO STANDARD'),
            dict(t='gap', h=30),
            dict(t='card', num='150', label='crediti nel triennio|2026-2028', size=170),
            dict(t='sub', text='al netto di esoneri, esenzioni e riduzioni', size=36, at='al netto')]),
        dict(at='se costruisci', items=[
            dict(t='chip', text='DOSSIER FORMATIVO INDIVIDUALE'),
            dict(t='gap', h=30),
            dict(t='card', num='+40', label='crediti di bonus|costruendolo sul portale Cogeaps', size=170, accent='sky')]),
        dict(at='i crediti mancanti', items=[
            dict(t='chip', text='TRIENNIO 2023-2025'),
            dict(t='gap', h=30),
            dict(t='card', num='31/12/2028', label='nuovo termine|per recuperare i crediti mancanti', size=112)]),
        dict(at='e per mantenere', items=[
            dict(t='chip', text='POLIZZA ASSICURATIVA 2026'),
            dict(t='gap', h=30),
            dict(t='card', num='70%', label='dei crediti 2023-2025|per mantenere attiva la copertura', size=170, accent='sky')]),
        dict(at='controlla oggi', items=[
            dict(t='gap', h=120),
            dict(t='stamp', text='Controlla la tua posizione', size=44),
            dict(t='gap', h=20),
            dict(t='sub', text='Condividilo con un collega', size=52, col='white', w='x', at='condividi')]),
    ])

SPECS['prean'] = dict(
    id='prean', voice=V + 'prean.mp3', asr=V + 'prean.json',
    foot=['Indicazioni generali di buona pratica preanalitica',
          'Valgono sempre le procedure del tuo laboratorio'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='PREANALITICA'),
            dict(t='gap', h=40),
            dict(t='title', text='Un errore|*preanalitico*|non si corregge|in laboratorio', size=104)]),
        dict(at='cinque controlli', items=[
            dict(t='chip', text='PRIMA DI OGNI PRELIEVO'),
            dict(t='gap', h=30),
            dict(t='title', text='*5* controlli|veloci', size=128),
            dict(t='gap', h=20),
            dict(t='row', n='1', text='Identità e etichetta', at='uno'),
            dict(t='row', n='2', text='Provetta giusta per l\'esame', at='due'),
            dict(t='row', n='3', text='Tecnica di prelievo', at='tre'),
            dict(t='row', n='4', text='Miscelazione e tempi', at='quattro'),
            dict(t='row', n='5', text='Condizioni di invio', at='cinque le')]),
        dict(at='sono indicazioni', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Quale ti fa perdere più tempo?', size=42),
            dict(t='gap', h=20),
            dict(t='sub', text='Scrivilo nei commenti', size=52, col='white', w='x', at='scrivilo')]),
    ])

SPECS['ves'] = dict(
    id='ves', voice=V + 'ves.mp3', asr=V + 'ves.json',
    foot=['Fonte: scheda tecnica del produttore · dati dichiarati dal produttore',
          'Dispositivo per uso professionale · reagenta.it'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='VES · ALCOR miniiSED'),
            dict(t='gap', h=40),
            dict(t='title', text='Quanti secondi|servono oggi|per un risultato|di *VES*?', size=108)]),
        dict(at='con la', items=[
            dict(t='chip', text='CON ALCOR miniiSED'),
            dict(t='gap', h=30),
            dict(t='card', num='~15 s', label='per un risultato di VES|direttamente da provetta', size=170)]),
        dict(at='usa', items=[
            dict(t='chip', text='REOLOGIA FOTOMETRICA'),
            dict(t='gap', h=30),
            dict(t='title', text='Misura|*l\'aggregazione*|dei globuli rossi', size=92),
            dict(t='gap', h=10),
            dict(t='sub', text='valore in mm/ora, correlato al metodo Westergren', size=36, at='con un')]),
        dict(at='analizza direttamente', items=[
            dict(t='chip', text='CAMPIONE'),
            dict(t='gap', h=30),
            dict(t='title', text='Provette primarie|*EDTA*', size=104),
            dict(t='gap', h=10),
            dict(t='sub', text='senza preparazione del campione', size=44, col='white', w='x', at='senza preparazione')]),
        dict(at='la produttività', items=[
            dict(t='chip', text='PRODUTTIVITÀ DICHIARATA'),
            dict(t='gap', h=30),
            dict(t='card', num='180', label='test all\'ora, fino a|dichiarati dal produttore', size=170, accent='sky'),
            dict(t='sub', text='in un ingombro ridotto', size=40, at='in un')]),
        dict(at='salva il', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Salva il video', size=46),
            dict(t='gap', h=20),
            dict(t='sub', text='per rivedere i flussi|del tuo laboratorio', size=48, col='white', w='x', at='per quando')]),
    ])

SPECS['resp'] = dict(
    id='resp', voice=V + 'resp.mp3', asr=V + 'resp.json',
    foot=['Fonti: legge 24/2017, art. 10; DM 232/2023 · informazioni generali',
          'Non è consulenza legale: verifica la tua polizza con un professionista'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='RESPONSABILITÀ PROFESSIONALE'),
            dict(t='gap', h=40),
            dict(t='title', text='Hai le tue|polizze|*in regola?*', size=116),
            dict(t='sub', text='Legge Gelli-Bianco, 24/2017', size=42, at='vediamo')]),
        dict(at='le strutture', items=[
            dict(t='chip', text='STRUTTURE SANITARIE'),
            dict(t='gap', h=30),
            dict(t='title', text='Copertura per la|*responsabilità civile*', size=84),
            dict(t='gap', h=20),
            dict(t='card', num='Marzo 2026', label='decreto attuativo operativo|(DM 232/2023)', size=104, accent='sky', at='il decreto')]),
        dict(at='se lavori', items=[
            dict(t='chip', text='SE LAVORI IN UNA STRUTTURA'),
            dict(t='gap', h=30),
            dict(t='card', num='Colpa grave', label='polizza personale, a tuo carico|legge 24/2017, art. 10, comma 3', size=100)]),
        dict(at='serve perché', items=[
            dict(t='chip', text='LA RIVALSA'),
            dict(t='gap', h=30),
            dict(t='title', text='La struttura può|*rivalersi su di te*', size=88),
            dict(t='gap', h=20),
            dict(t='stamp', text='solo per dolo o colpa grave', size=40, at='ma solo')]),
        dict(at='se eserciti', items=[
            dict(t='chip', text='LIBERO PROFESSIONISTA'),
            dict(t='gap', h=30),
            dict(t='title', text='Serve la *tua*|assicurazione|di responsabilità civile', size=84),
            dict(t='gap', h=10),
            dict(t='sub', text='anche se assumi un obbligo|direttamente con il paziente', size=40, at='assumi')]),
        dict(at='controlla cosa', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Controlla la tua polizza', size=46),
            dict(t='gap', h=20),
            dict(t='sub', text='Condividilo con un collega', size=52, col='white', w='x', at='condividi')]),
    ])
