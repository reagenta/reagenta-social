V = '/home/claude/work/voice/'
SPECS = {}

SPECS['ecm'] = dict(
    theme='ecm', id='ecm', voice=V + 'ecm.mp3', asr=V + 'ecm.json',
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
    theme='prean', id='prean', voice=V + 'prean.mp3', asr=V + 'prean.json',
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
    theme='ves', id='ves', voice=V + 'ves.mp3', asr=V + 'ves.json',
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
            dict(t='card', num='180', label='test all\'ora, valore massimo|dichiarato dal produttore', size=170, accent='sky'),
            dict(t='sub', text='in un ingombro ridotto', size=40, at='in un')]),
        dict(at='salva il', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Salva il video', size=46),
            dict(t='gap', h=20),
            dict(t='sub', text='per rivedere i flussi|del tuo laboratorio', size=48, col='white', w='x', at='per quando')]),
    ])

SPECS['resp'] = dict(
    theme='resp', id='resp', voice=V + 'resp.mp3', asr=V + 'resp.json',
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

SPECS['s900'] = dict(
    theme='s900', id='s900', voice=V + 's900.mp3', asr=V + 's900.json',
    foot=['Fonte: scheda tecnica del produttore · dati dichiarati dal produttore',
          'Dispositivo per uso professionale · reagenta.it'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='CHEMILUMINESCENZA · AUTOLUMO S900'),
            dict(t='gap', h=40),
            dict(t='title', text='Quanto può fare|un analizzatore|di *chemiluminescenza*|in laboratorio?', size=92)]),
        dict(at='fino a', items=[
            dict(t='chip', text='PRODUTTIVITÀ DICHIARATA'),
            dict(t='gap', h=30),
            dict(t='card', num='180', label='test all\'ora, valore massimo|dichiarato dal produttore', size=170)]),
        dict(at='cinquantuno', items=[
            dict(t='chip', text='POSIZIONI CAMPIONE'),
            dict(t='gap', h=30),
            dict(t='card', num='51', label='posizioni campione|di cui 3 per i campioni urgenti', size=170, accent='sky')]),
        dict(at='sedici', items=[
            dict(t='chip', text='REAGENTI'),
            dict(t='gap', h=30),
            dict(t='card', num='16', label='posizioni refrigerate|per i reagenti', size=170)]),
        dict(at='oltre', items=[
            dict(t='chip', text='MENU ANALITICO'),
            dict(t='gap', h=30),
            dict(t='card', num='150+', label='parametri disponibili|dalla tiroide ai marcatori tumorali', size=150, accent='sky'),
            dict(t='sub', text='dalle malattie infettive all\'autoimmunità', size=36, at='dalle malattie')]),
        dict(at='consegna', items=[
            dict(t='chip', text='REAGENTA'),
            dict(t='gap', h=30),
            dict(t='row', n='1', text='Consegna veloce', at='consegna'),
            dict(t='row', n='2', text='Magazzino sempre disponibile', at='magazzino'),
            dict(t='row', n='3', text='Assistenza tecnica in 48 ore', at='assistenza')]),
        dict(at='scrivici', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Richiedi una presentazione', size=46),
            dict(t='gap', h=20),
            dict(t='sub', text='reagenta.it', size=52, col='white', w='x', at='presentazione')]),
    ])

SPECS['assist'] = dict(
    theme='assist', id='assist', voice=V + 'assist.mp3', asr=V + 'assist.json',
    foot=['Hotline: lun-ven 8:30-18:00 · tel. 081 8045042 · reagenta.it/assistenza',
          'Tempi di intervento con contratto di assistenza attivo'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='ASSISTENZA TECNICA'),
            dict(t='gap', h=40),
            dict(t='title', text='Strumento|*fermo?*', size=128),
            dict(t='sub', text='Cosa succede dopo la tua chiamata', size=44, at='cosa succede')]),
        dict(at='uno', items=[
            dict(t='chip', text='PASSO 1'),
            dict(t='gap', h=30),
            dict(t='title', text='Chiami o|apri un *ticket*', size=96),
            dict(t='gap', h=10),
            dict(t='sub', text='081 8045042 · reagenta.it/assistenza', size=38, at='oppure')]),
        dict(at='la hotline', items=[
            dict(t='chip', text='HOTLINE'),
            dict(t='gap', h=30),
            dict(t='card', num='8:30-18:00', label='dal lunedì al venerdì', size=120, accent='sky')]),
        dict(at='due', items=[
            dict(t='chip', text='PASSO 2'),
            dict(t='gap', h=30),
            dict(t='title', text='Email di|*presa in carico*', size=100),
            dict(t='gap', h=10),
            dict(t='sub', text='con la priorità che hai indicato', size=40, at='con la priorità')]),
        dict(at="l'intervento", items=[
            dict(t='chip', text='PASSO 3'),
            dict(t='gap', h=30),
            dict(t='card', num='24-48 ore', label='arrivo dell\'intervento', size=130)]),
        dict(at='con un contratto', items=[
            dict(t='chip', text='CON CONTRATTO ATTIVO'),
            dict(t='gap', h=30),
            dict(t='title', text='*Coda prioritaria*|livelli di servizio|garantiti', size=86)]),
        dict(at='chiama', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='081 8045042', size=60),
            dict(t='gap', h=20),
            dict(t='sub', text='Quando serve', size=52, col='white', w='x', at='quando')]),
    ])

SPECS['rischio'] = dict(
    theme='rischio', id='rischio', voice=V + 'rischio.mp3', asr=V + 'rischio.json',
    foot=['Indicazioni generali · fonte: D.Lgs. 81/2008',
          'Segui sempre la procedura della tua struttura'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='RISCHIO BIOLOGICO'),
            dict(t='gap', h=40),
            dict(t='title', text='Puntura|*accidentale*|in laboratorio', size=110),
            dict(t='sub', text='Cosa fare subito', size=46, at='cosa fare')]),
        dict(at='lava', items=[
            dict(t='chip', text='PASSO 1'),
            dict(t='gap', h=30),
            dict(t='title', text='*Lava* con acqua|e sapone', size=96),
            dict(t='gap', h=10),
            dict(t='sub', text='lascia sanguinare la ferita e disinfetta', size=38, at='lascia')]),
        dict(at='avvisa', items=[
            dict(t='chip', text='PASSO 2'),
            dict(t='gap', h=30),
            dict(t='title', text='*Avvisa subito*|datore di lavoro|o preposto', size=92),
            dict(t='gap', h=10),
            dict(t='sub', text='segnalazione immediata: obbligo del D.Lgs. 81/2008', size=36, at='la segnalazione')]),
        dict(at='vai', items=[
            dict(t='chip', text='PASSO 3'),
            dict(t='gap', h=30),
            dict(t='title', text='Pronto soccorso|o *medico competente*', size=88),
            dict(t='gap', h=10),
            dict(t='sub', text='la profilassi post-esposizione va iniziata|il prima possibile', size=38, at='la profilassi')]),
        dict(at='il datore di lavoro deve', items=[
            dict(t='chip', text='IL DATORE DI LAVORO DEVE GARANTIRE'),
            dict(t='gap', h=30),
            dict(t='row', n='·', text='Cure immediate', at='cure'),
            dict(t='row', n='·', text='Esami medici', at='esami'),
            dict(t='row', n='·', text='Se serve, assistenza psicologica', at='assistenza')]),
        dict(at='segui sempre', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Segui la procedura della tua struttura', size=40),
            dict(t='gap', h=20),
            dict(t='sub', text='Condividilo con un collega', size=52, col='white', w='x', at='condividi')]),
    ])

SPECS['hp'] = dict(
    theme='hp', id='hp', voice=V + 'hp.mp3', asr=V + 'hp.json',
    foot=['Indicazioni generali · test rapido per uso professionale',
          'Il risultato va interpretato da personale qualificato'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='MITO'),
            dict(t='gap', h=40),
            dict(t='title', text='Per un test rapido|*H. pylori*|serve uno strumento', size=92)]),
        dict(at='fatto', items=[
            dict(t='chip', text='FATTO'),
            dict(t='gap', h=30),
            dict(t='title', text='*No.*', size=200),
            dict(t='gap', h=10),
            dict(t='sub', text='una cassetta, lettura visiva', size=44, at='il test')]),
        dict(at='in cinque', items=[
            dict(t='chip', text='TEST RAPIDO'),
            dict(t='gap', h=30),
            dict(t='card', num='5 min', label='lettura visiva|nessuna strumentazione richiesta', size=150, accent='sky')]),
        dict(at='è un', items=[
            dict(t='chip', text='CAMPIONE'),
            dict(t='gap', h=30),
            dict(t='title', text='Test su *feci*|per uso professionale', size=92)]),
        dict(at='può essere', items=[
            dict(t='chip', text='IN AMBULATORIO E LABORATORIO'),
            dict(t='gap', h=30),
            dict(t='title', text='Screening|di *prima linea*', size=104)]),
        dict(at='il risultato', items=[
            dict(t='chip', text='ATTENZIONE'),
            dict(t='gap', h=30),
            dict(t='title', text='Interpretato da|*personale qualificato*', size=88),
            dict(t='gap', h=10),
            dict(t='sub', text='e, se necessario, confermato', size=44, at='e se necessario')]),
        dict(at='quale test', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Quale test rapido usi di più?', size=44),
            dict(t='gap', h=20),
            dict(t='sub', text='Raccontacelo nei commenti', size=52, col='white', w='x', at='racconta')]),
    ])

SPECS['campania'] = dict(
    theme='campania', id='campania', voice=V + 'campania.mp3', asr=V + 'campania.json',
    foot=['Esperienza presso il Consorzio Campanialab, Camposano (NA)',
          'Informazioni generali · reagenta.it'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='CASO REALE'),
            dict(t='gap', h=40),
            dict(t='title', text='*Due* sistemi,|un solo flusso', size=118)]),
        dict(at='com\'è andata', items=[
            dict(t='chip', text='CONSORZIO CAMPANIALAB'),
            dict(t='gap', h=30),
            dict(t='title', text='Camposano (NA)', size=100),
            dict(t='sub', text='com\'è andata', size=44, at='com\'è')]),
        dict(at='installazione', items=[
            dict(t='chip', text='IL PERCORSO'),
            dict(t='gap', h=30),
            dict(t='row', n='1', text='Installazione e validazione', at='installazione'),
            dict(t='row', n='2', text='Corso di formazione', at='un corso'),
            dict(t='row', n='3', text='Conferenza', at='una conferenza')]),
        dict(at='presentati', items=[
            dict(t='chip', text='PRESENTATI'),
            dict(t='gap', h=30),
            dict(t='card', num='AVE 562', label='automazione e parassitologia', size=130, accent='sky'),
            dict(t='sub', text='e un sistema da banco', size=40, at='e il sistema')]),
        dict(at='integra', items=[
            dict(t='chip', text='SOLUZIONI QUANTITATIVE AUTOMATICHE'),
            dict(t='gap', h=30),
            dict(t='row', n='·', text='Sangue occulto fecale', at='sangue'),
            dict(t='row', n='·', text='Calprotectina', at='cal protect'),
            dict(t='row', n='·', text='Helicobacter pylori', at='helicobacter')]),
        dict(at='vuoi un', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Un percorso simile nel tuo laboratorio?', size=40),
            dict(t='gap', h=20),
            dict(t='sub', text='Scrivici', size=52, col='white', w='x', at='scrivici')]),
    ])

SPECS['turni'] = dict(
    theme='turni', id='turni', voice=V + 'turni.mp3', asr=V + 'turni.json',
    foot=['Fonte: D.Lgs. 66/2003 · informazioni generali',
          'Valgono anche le previsioni del tuo contratto'],
    scenes=[
        dict(at='', items=[
            dict(t='chip', text='ORARIO DI LAVORO'),
            dict(t='gap', h=40),
            dict(t='title', text='Turni, riposi|e *reperibilità*', size=104),
            dict(t='sub', text='cosa dice la legge', size=44, at='cosa dice')]),
        dict(at='il decreto', items=[
            dict(t='chip', text='RIPOSO GIORNALIERO'),
            dict(t='gap', h=30),
            dict(t='card', num='11 ore', label='di riposo consecutivo|ogni 24 ore', size=150)]),
        dict(at='la durata', items=[
            dict(t='chip', text='ORARIO SETTIMANALE'),
            dict(t='gap', h=30),
            dict(t='card', num='48 ore', label='durata media massima|straordinario compreso', size=150, accent='sky')]),
        dict(at='il riposo settimanale', items=[
            dict(t='chip', text='RIPOSO SETTIMANALE'),
            dict(t='gap', h=30),
            dict(t='card', num='24 ore', label='consecutive|da sommare alle 11 giornaliere', size=150)]),
        dict(at='oltre le', items=[
            dict(t='chip', text='PAUSA'),
            dict(t='gap', h=30),
            dict(t='title', text='Oltre *6 ore*|di lavoro continuato', size=92),
            dict(t='gap', h=10),
            dict(t='sub', text='senza previsione contrattuale: almeno 10 minuti', size=38, at='in assenza')]),
        dict(at='la reperibilità', items=[
            dict(t='chip', text='REPERIBILITÀ'),
            dict(t='gap', h=30),
            dict(t='title', text='*Passiva:* non è|orario di lavoro', size=88),
            dict(t='gap', h=10),
            dict(t='sub', text='quella attiva sì', size=44, at='quella attiva')]),
        dict(at='i contratti', items=[
            dict(t='chip', text='DEROGHE'),
            dict(t='gap', h=30),
            dict(t='title', text='I contratti collettivi|possono *derogare*|nei limiti di legge', size=76)]),
        dict(at='verifica', items=[
            dict(t='gap', h=100),
            dict(t='stamp', text='Verifica cosa prevede il tuo', size=44),
            dict(t='gap', h=20),
            dict(t='sub', text='Condividilo con un collega', size=52, col='white', w='x', at='condividi')]),
    ])
