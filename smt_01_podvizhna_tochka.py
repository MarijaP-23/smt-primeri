import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="СМТ – Броеви со подвижна точка")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import struct
    from fractions import Fraction
    from decimal import Decimal, getcontext, localcontext, ROUND_HALF_EVEN, ROUND_DOWN

    getcontext().prec = 80
    plt.rcParams.update({"figure.dpi": 110, "axes.grid": True, "grid.alpha": 0.3})
    return (
        Decimal,
        Fraction,
        ROUND_DOWN,
        ROUND_HALF_EVEN,
        localcontext,
        mo,
        np,
        plt,
        struct,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Претставување на броеви на компјутер
    ### Илустративни примери – Симулациски методи во телекомуникациите

    Тетратката ги следи деловите **1.1 – 1.6** од скриптата. Секој пример е интерактивен:
    менувајте ги параметрите и набљудувајте што се случува.

    | Дел | Тема | Пример во тетратката |
    |---|---|---|
    | 1.1 | Општ облик $x=\pm d_0.d_1\cdots d_{p-1}\times\beta^e$ | „Играчка“ систем со подвижна точка на бројна оска |
    | 1.1 | Фиксна vs подвижна точка | $0.120\times0.120$ со 3 цифри |
    | 1.2 | Бинарен систем | Бинарна претстава на 0.1 и заокружување на $p$ бити |
    | 1.3–1.4 | Заокружување и грешка | Релативна грешка $\delta$ и граница $u=\tfrac12\beta^{1-p}$ |
    | 1.5 | IEEE 754 | Битови S, E, M за произволен број |
    | 1.6 | Аритметика | Собирање декадно (пр. 13) и бинарно (пр. 14) чекор по чекор |
    | + | Зошто е важно за симулации | Акумулирање на време $t \mathrel{+}= \Delta t$, фаза на носител |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.1 Општ облик на број со подвижна точка

    $$x = \pm\, d_0.d_1 d_2\cdots d_{p-1}\times \beta^{e},\qquad 0\le d_i\le\beta-1,\quad e_{\min}\le e\le e_{\max}$$

    Ако $d_0\neq 0$ бројот е **нормализиран**. Да ги нацртаме **сите** позитивни нормализирани броеви
    на еден мал („играчка“) систем. Обрнете внимание: броевите **не се рамномерно распоредени** –
    растојанието меѓу соседни броеви се зголемува $\beta$ пати при секој нов експонент.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    toy_beta = mo.ui.dropdown(options={"2": 2, "3": 3, "10": 10}, value="2", label="Основа β")
    toy_p = mo.ui.slider(1, 5, value=3, label="Број цифри p", show_value=True)
    toy_emin = mo.ui.slider(-3, 0, value=-1, label="e_min", show_value=True)
    toy_emax = mo.ui.slider(0, 3, value=2, label="e_max", show_value=True)
    toy_log = mo.ui.checkbox(value=False, label="Логаритамска оска")
    mo.hstack([toy_beta, toy_p, toy_emin, toy_emax, toy_log], justify="start", gap=1.5)
    return toy_beta, toy_emax, toy_emin, toy_log, toy_p


@app.cell(hide_code=True)
def _(Fraction):
    def toy_numbers(beta, p, emin, emax):
        """Сите позитивни нормализирани броеви: m * beta^(e-p+1), m ∈ [beta^(p-1), beta^p - 1]  (изр. 1.2)."""
        out = []
        for e in range(emin, emax + 1):
            for m in range(beta ** (p - 1), beta**p):
                out.append((Fraction(m) * Fraction(beta) ** (e - p + 1), e))
        return out

    def toy_round(x, beta, p, emin, emax):
        """Заокружување до најблискиот број во системот (при еднаквост – парна мантиса)."""
        x = Fraction(x)
        if x == 0:
            return Fraction(0)
        s = 1 if x > 0 else -1
        ax = abs(x)
        e = 0
        while ax >= Fraction(beta) ** (e + 1):
            e += 1
        while ax < Fraction(beta) ** e:
            e -= 1
        e = max(e, emin)
        scale = Fraction(beta) ** (e - p + 1)
        q = ax / scale
        m = q.numerator // q.denominator
        r = q - m
        if r > Fraction(1, 2) or (r == Fraction(1, 2) and m % 2 == 1):
            m += 1
        if m == beta**p:
            m, e = beta ** (p - 1), e + 1
            scale = Fraction(beta) ** (e - p + 1)
        xmax = Fraction(beta) ** emax * (beta - Fraction(beta) ** (-p + 1))
        val = m * scale
        return s * min(val, xmax)

    return toy_numbers, toy_round


@app.cell(hide_code=True)
def _(mo, np, plt, toy_beta, toy_emax, toy_emin, toy_log, toy_numbers, toy_p):
    _b, _p, _e1, _e2 = toy_beta.value, toy_p.value, toy_emin.value, toy_emax.value
    _nums = toy_numbers(_b, _p, _e1, _e2)
    _vals = np.array([float(v) for v, _ in _nums])
    _exps = np.array([e for _, e in _nums])

    _fig, _ax = plt.subplots(figsize=(10, 2.4))
    _cmap = plt.get_cmap("tab10")
    for _i, _e in enumerate(range(_e1, _e2 + 1)):
        _sel = _exps == _e
        _ax.vlines(_vals[_sel], 0, 1, color=_cmap(_i % 10), lw=1.6, label=f"e = {_e}")
    _ax.vlines(0, 0, 1, color="k", lw=2)
    _ax.set_yticks([])
    _ax.set_ylim(0, 1.25)
    if toy_log.value:
        _ax.set_xscale("log")
    _ax.set_title(f"Позитивни нормализирани броеви: β={_b}, p={_p}, e ∈ [{_e1}, {_e2}]")
    _ax.legend(ncol=min(8, _e2 - _e1 + 1), loc="upper center", fontsize=8, frameon=False,
               bbox_to_anchor=(0.5, -0.25))
    _fig.tight_layout()

    _xmin = float(_b) ** _e1
    _xmax = float(_b) ** _e2 * (_b - float(_b) ** (-_p + 1))
    _total = 2 * len(_nums)
    _bits = np.log2(_e2 - _e1 + 1) + _p * np.log2(_b) + 1

    mo.vstack([
        _fig,
        mo.md(f"""
    - Најмал позитивен нормализиран: $x_{{\\min}} = \\beta^{{e_{{\\min}}}} = {_xmin:g}$
    - Најголем: $x_{{\\max}} = \\beta^{{e_{{\\max}}}}(\\beta-\\beta^{{-p+1}}) = {_xmax:g}$
    - Број позитивни нормализирани вредности: **{len(_nums)}** (со знак: {_total}, плус нулата која **не** може да се претстави нормализирано)
    - Отприлика потребни бити (сп. изр. 1.6): $\\log_2(e_{{\\max}}-e_{{\\min}}+1)+p\\log_2\\beta+1 \\approx {_bits:.2f}$
    - Празнина околу нулата: меѓу $0$ и $x_{{\\min}}$ нема ниту еден број!
    """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.1 (пр. 3) Фиксна наспроти подвижна точка

    Имаме само **3 цифри**. Кај фиксна точка, точката е секогаш меѓу 1-та и 2-та цифра (облик `d.dd`),
    кај подвижна точка имаме 3 **значајни** цифри и посебен експонент.
    Скриптата го зема примерот $0.120\times0.120$: со фиксна точка се добива $0.01$, а точното е $0.0144$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fx_a = mo.ui.text(value="0.120", label="a")
    fx_b = mo.ui.text(value="0.120", label="b")
    fx_digits = mo.ui.slider(2, 6, value=3, label="Број цифри", show_value=True)
    mo.hstack([fx_a, fx_b, fx_digits], justify="start", gap=1.5)
    return fx_a, fx_b, fx_digits


@app.cell(hide_code=True)
def _(Decimal, ROUND_HALF_EVEN, fx_a, fx_b, fx_digits, localcontext, mo):
    def _fixed(x, nd):
        # формат d.ddd… : nd-1 децимали после точката
        return x.quantize(Decimal(1).scaleb(-(nd - 1)), rounding=ROUND_HALF_EVEN)

    def _flt(x, nd):
        with localcontext() as _c:
            _c.prec = nd
            _c.rounding = ROUND_HALF_EVEN
            return +x

    try:
        _a, _b = Decimal(fx_a.value), Decimal(fx_b.value)
        _n = fx_digits.value
        _exact = _a * _b
        _fx = _fixed(_fixed(_a, _n) * _fixed(_b, _n), _n)
        _fl = _flt(_flt(_a, _n) * _flt(_b, _n), _n)

        def _rel(v):
            return "—" if _exact == 0 else f"{abs((v - _exact) / _exact) * 100:.3g} %"

        _out = mo.md(f"""
    | | Резултат | Релативна грешка |
    |---|---|---|
    | Точно | `{_exact}` | 0 |
    | Фиксна точка (`d.{'d' * (_n - 1)}`) | `{_fx}` | {_rel(_fx)} |
    | Подвижна точка ({_n} значајни цифри) | `{_fl:.{_n - 1}E}` | {_rel(_fl)} |

    Пробајте: `a = 0.0012`, `b = 0.0034` – фиксната точка дава **нула**, подвижната скоро точен резултат.
    Кај фиксна точка опсегот е ограничен (`d.dd` не може да претстави ни 10), додека подвижната точка лесно ја „пренесува“ големината во експонентот.
    """)
    except Exception:
        _out = mo.md("⚠️ Внесете валидни децимални броеви.")
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.2 Бинарен систем – зошто 0.1 не е точно 0.1

    Бројот $0.1$ има **конечна** декадна, но **бесконечна** бинарна претстава (изр. 1.7):
    $$(0.1)_{10} = (0.000110011001100\ldots)_2$$
    Мантисата се заокружува на $p$ бити, па зачуваната вредност е само приближна (изр. 1.8–1.10).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    bin_x = mo.ui.text(value="0.1", label="Декаден број x")
    bin_p = mo.ui.slider(4, 60, value=24, label="Бити за мантиса p", show_value=True)
    mo.hstack([bin_x, bin_p], justify="start", gap=1.5)
    return bin_p, bin_x


@app.cell(hide_code=True)
def _(Fraction):
    def binary_expansion(x, nfrac=60):
        """Бинарна претстава на позитивен рационален број: (цел дел, низа од nfrac бити по точката)."""
        x = Fraction(x)
        ip = x.numerator // x.denominator
        fr = x - ip
        bits = []
        for _ in range(nfrac):
            fr *= 2
            b = 1 if fr >= 1 else 0
            bits.append(str(b))
            fr -= b
        return bin(ip)[2:], "".join(bits), fr == 0

    def round_to_p_bits(x, p):
        """Нормализирано: x = 1.m × 2^e, мантисата заокружена на p бити (ties-to-even)."""
        x = Fraction(x)
        e = 0
        while x >= 2 ** (e + 1):
            e += 1
        while x < Fraction(2) ** e:
            e -= 1
        q = x / Fraction(2) ** (e - p + 1)          # во [2^(p-1), 2^p)
        m = q.numerator // q.denominator
        r = q - m
        if r > Fraction(1, 2) or (r == Fraction(1, 2) and m % 2):
            m += 1
        if m == 2**p:
            m, e = 2 ** (p - 1), e + 1
        return m, e, Fraction(m) * Fraction(2) ** (e - p + 1)

    return binary_expansion, round_to_p_bits


@app.cell(hide_code=True)
def _(
    Decimal,
    Fraction,
    bin_p,
    bin_x,
    binary_expansion,
    mo,
    round_to_p_bits,
):
    try:
        _x = Fraction(bin_x.value.strip())
        assert _x > 0
        _ip, _fb, _finite = binary_expansion(_x, 64)
        _p = bin_p.value
        _m, _e, _xr = round_to_p_bits(_x, _p)
        _mbits = bin(_m)[2:]
        _dots = '' if _finite else r'\ldots'
        _exact_dec = Decimal(_xr.numerator) / Decimal(_xr.denominator)
        _delta = abs((_xr - _x) / _x)
        _u = Fraction(1, 2) * Fraction(2) ** (1 - _p)
        # точна (бесконечна) мантиса за прикажување
        _m_long, _, _ = round_to_p_bits(_x, 80)
        _mlong = bin(_m_long)[2:]
        _diff = "".join(
            f"<span style='color:#c0392b;font-weight:bold'>{c}</span>" if i < len(_mbits) and c != _mbits[i] else c
            for i, c in enumerate(_mlong[: len(_mbits)])
        )
        _out = mo.md(f"""
    **Бинарно:** $({bin_x.value})_{{10}} = ({_ip}.{_fb}{_dots})_2$
    {'✅ конечна претстава – бројот е точно претставлив' if _finite else '♾️ бесконечна (периодична) претстава'}

    **Нормализирано** $x = 1.m \\times 2^{{e}}$, $e = {_e}$:

    <pre style="font-size:0.95em">
    точна мантиса      : {_mlong[:len(_mbits)]}<span style="color:#888">{_mlong[len(_mbits):len(_mbits)+16]}…</span>
    заокружена ({_p:>2} b) : {_mbits}
    </pre>

    **Зачувана вредност** $m'\\times2^{{e}}$ = `{_exact_dec:.40f}`…

    Релативна грешка $\\delta = |x^*-x|/|x|$ = **{float(_delta):.3e}** ≤ $u = 2^{{-{_p}}}$ = {float(_u):.3e} ✔

    *(За 0.1 и p = 24 добиваме 0.100000001490116119384765625 – исто како изр. 1.10 во скриптата.)*
    """)
    except Exception:
        _out = mo.md("⚠️ Внесете позитивен декаден број (пр. `0.1`, `0.25`, `3.3`, `1/3`).")
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.3 – 1.4 Заокружување и грешка при заокружување

    Секој реален број $x$ се заменува со најблискиот број $x^*$ од системот (при еднакво растојание – оној со **парна** мантиса).
    Релативната грешка е ограничена со **единичната грешка на заокружување**:

    $$\delta = \left|\frac{x^*-x}{x}\right| \le u = \tfrac12\beta^{1-p},\qquad x^* = x(1+\delta)\quad (1.11–1.14)$$

    На графикот е $\delta(x)$ за „играчка“ системот од горе (β, p, e_min, e_max се исти).
    Забележете ја **пилестата** форма: грешката е 0 точно на претставливите броеви, а највисока на средина меѓу нив;
    апсолутната грешка расте со $x$, но релативната останува под $u$.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np, plt, toy_beta, toy_emax, toy_emin, toy_p, toy_round):
    _b, _p, _e1, _e2 = toy_beta.value, toy_p.value, toy_emin.value, toy_emax.value
    _xmin = float(_b) ** _e1
    _xmax = float(_b) ** _e2 * (_b - float(_b) ** (-_p + 1))
    _xs = np.geomspace(_xmin, _xmax, 3000)
    _xr = np.array([float(toy_round(v, _b, _p, _e1, _e2)) for v in _xs])
    _abs = np.abs(_xr - _xs)
    _rel = _abs / _xs
    _u = 0.5 * _b ** (1 - _p)

    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(11, 3.3))
    _a1.plot(_xs, _abs, lw=1)
    _a1.set_title("Апсолутна грешка |x* − x|")
    _a1.set_xlabel("x")
    _a2.plot(_xs, _rel, lw=1, label="δ(x)")
    _a2.axhline(_u, color="C3", ls="--", label=f"u = ½β^(1−p) = {_u:g}")
    _a2.set_title("Релативна грешка δ")
    _a2.set_xlabel("x")
    _a2.set_xscale("log")
    _a2.legend(fontsize=8)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Заокружување кон парна мантиса („ties to even“)** – што кога $x$ е точно на половина меѓу два броја?
    Пример во декаден систем со $p=2$:
    """)
    return


@app.cell(hide_code=True)
def _(Decimal, ROUND_HALF_EVEN, localcontext, mo):
    _rows = []
    for _s in ["1.25", "1.35", "1.45", "1.55", "2.65", "2.75"]:
        with localcontext() as _c:
            _c.prec = 2
            _c.rounding = ROUND_HALF_EVEN
            _r = +Decimal(_s)
        _rows.append(f"| {_s} | {_r} | {'парна ✓' if int(str(_r)[-1]) % 2 == 0 else ''} |")
    mo.md("| x | x* (p=2) | последна цифра |\n|---|---|---|\n" + "\n".join(_rows) +
          "\n\nНа овој начин грешките при заокружување не се **систематски** во една насока (средната вредност ≈ 0) – важно кога се собираат милиони примероци во симулација.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.5 IEEE 754 – како компјутерот навистина го зачувува бројот

    $$\underbrace{S}_{1\text{ бит}}\;\Big|\;\underbrace{E}_{8\,/\,11\text{ бити}}\;\Big|\;\underbrace{M}_{23\,/\,52\text{ бити}}
    \qquad x = (-1)^S\left(1+\frac{M}{2^{23}}\right)2^{E-127}\quad(1.18)$$

    Првата цифра на нормализираната мантиса е секогаш 1 и **не се зачувува** („скриен бит“), па $p = 24$ односно $p=53$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ieee_x = mo.ui.text(value="0.1", label="Број x")
    ieee_fmt = mo.ui.radio(options=["единична (float32)", "двојна (float64)"], value="единична (float32)", inline=True)
    mo.hstack([ieee_x, ieee_fmt], justify="start", gap=2)
    return ieee_fmt, ieee_x


@app.cell(hide_code=True)
def _(Decimal, Fraction, ieee_fmt, ieee_x, mo, np, struct):
    def _bits_of(x, single):
        if single:
            return format(struct.unpack(">I", struct.pack(">f", x))[0], "032b")
        return format(struct.unpack(">Q", struct.pack(">d", x))[0], "064b")

    try:
        _single = ieee_fmt.value.startswith("един")
        _txt = ieee_x.value.strip()
        _xv = float(_txt)
        _stored = float(np.float32(_xv)) if _single else _xv
        _bits = _bits_of(_xv, _single)
        _ne, _nm, _bias = (8, 23, 127) if _single else (11, 52, 1023)
        _S, _E, _M = _bits[0], _bits[1 : 1 + _ne], _bits[1 + _ne :]
        _Ei, _Mi = int(_E, 2), int(_M, 2)

        _box = (
            "<div style='font-family:monospace;font-size:1.05em;line-height:1.9'>"
            f"<span style='background:#f5b7b1;padding:3px 5px;border-radius:3px' title='знак'>{_S}</span> "
            f"<span style='background:#aed6f1;padding:3px 5px;border-radius:3px' title='експонент'>{_E}</span> "
            f"<span style='background:#abebc6;padding:3px 5px;border-radius:3px;word-break:break-all' title='мантиса'>{_M}</span>"
            "<br><small>&nbsp;<b style='color:#c0392b'>S</b> &nbsp; <b style='color:#2471a3'>E</b> (поместен експонент) &nbsp; "
            "<b style='color:#1e8449'>M</b> (мантиса без скриениот бит)</small></div>"
        )
        if _Ei == 0 and _Mi == 0:
            _interp = "Ова е **нула** (специјален случај: E = 0, M = 0)."
        elif _Ei == 2**_ne - 1:
            _interp = "Ова е **±∞ или NaN** (специјален случај: E = сите единици) – надвор од опсегот."
        elif _Ei == 0:
            _interp = "Ова е **субнормален** број (E = 0): помал од $x_{\\min}$, нема скриен бит – надвор од рамката на скриптата."
        else:
            _e = _Ei - _bias
            _exactv = Decimal(_stored)
            try:
                _xe = Fraction(_txt)
                _delta = float(abs((Fraction(_stored) - _xe) / _xe)) if _xe != 0 else 0.0
            except Exception:
                _delta = float("nan")
            _u = 2.0 ** -(_nm + 1)
            _interp = f"""
    - $S = {_S}$ → знак **{'−' if _S == '1' else '+'}**
    - $E = ({_E})_2 = {_Ei}$ → $e = E - {_bias} = {_e}$
    - $M = {_Mi}$ → мантиса $1 + M/2^{{{_nm}}} = {1 + _Mi / 2**_nm:.17g}$
    - $x^* = {'-' if _S == '1' else ''}{1 + _Mi / 2**_nm:.17g}\\times 2^{{{_e}}}$
    - **Точна зачувана вредност:** `{_exactv}`
    - Релативна грешка $\\delta$ = **{_delta:.3e}** ≤ $u = 2^{{-{_nm + 1}}}$ ≈ {_u:.3e}
    """
        _out = mo.vstack([mo.Html(_box), mo.md(_interp)])
    except Exception:
        _out = mo.md("⚠️ Внесете број, на пр. `0.1`, `-6.5`, `100`, `1e-40`, `1e39`.")
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Прецизност | Вк. бити | Мантиса | Експонент | $u$ | $e_{\min}$ / $e_{\max}$ | Опсег | Декадни цифри |
    |---|---|---|---|---|---|---|---|
    | Единична | 32 | 23 + 1 | 8 | $2^{-24}\approx5.96\cdot10^{-8}$ | −126 / +127 | $10^{\pm38}$ | ≈ 7–8 |
    | Двојна | 64 | 52 + 1 | 11 | $2^{-53}\approx1.11\cdot10^{-16}$ | −1022 / +1023 | $10^{\pm308}$ | ≈ 15–16 |

    Пробајте: `1`, `2`, `0.25`, `100` (точни); `0.1`, `0.2`, `3.14159` (приближни); `16777217` во float32 ($2^{24}+1$ – веќе не е претставлив!).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.6 Аритметика со подвижна точка

    ### Пример 13 – декадно собирање со $p$ цифри
    Чекори: (1) изедначување на експонентите, (2) собирање, (3) нормализација и заокружување.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    dec_a = mo.ui.text(value="123456.7", label="a")
    dec_b = mo.ui.text(value="101.7654", label="b")
    dec_p = mo.ui.slider(2, 12, value=7, label="p (декадни цифри)", show_value=True)
    mo.hstack([dec_a, dec_b, dec_p], justify="start", gap=1.5)
    return dec_a, dec_b, dec_p


@app.cell(hide_code=True)
def _(Decimal, ROUND_HALF_EVEN, dec_a, dec_b, dec_p, localcontext, mo):
    def _norm(x):
        _e = x.adjusted()
        return x.scaleb(-_e), _e

    try:
        _p = dec_p.value
        with localcontext() as _c:
            _c.prec = _p
            _c.rounding = ROUND_HALF_EVEN
            _a, _b = +Decimal(dec_a.value), +Decimal(dec_b.value)
        _ma, _ea = _norm(_a)
        _mb, _eb = _norm(_b)
        _E = max(_ea, _eb)
        _sa, _sb = _a.scaleb(-_E), _b.scaleb(-_E)
        _sum_exact = _a + _b
        _ms, _es = _norm(_sum_exact)
        with localcontext() as _c:
            _c.prec = _p
            _c.rounding = ROUND_HALF_EVEN
            _sum_r = +_sum_exact
        _mr, _er = _norm(_sum_r)
        _delta = abs((_sum_r - _sum_exact) / _sum_exact) if _sum_exact else 0
        _u = Decimal("0.5") * Decimal(10) ** (1 - _p)
        _w = 22
        _pre = "\n".join([
            f"1) изедначување на експонент 10^{_E}:",
            f"      {str(_sa):>{_w}} × 10^{_E}",
            f"    + {str(_sb):>{_w}} × 10^{_E}",
            f"    {'-' * (_w + 2)}",
            f"2)    {str(_sum_exact.scaleb(-_E)):>{_w}} × 10^{_E}   (точен збир)",
            f"3) нормализација + заокружување на {_p} цифри:",
            f"      x* = {_mr} × 10^{_er}",
        ])
        _out = mo.vstack([
            mo.md(f"Влез (веќе заокружен на {_p} цифри): $a = {_ma}\\times10^{{{_ea}}}$, $b = {_mb}\\times10^{{{_eb}}}$"),
            mo.Html(f"<pre>{_pre}</pre>"),
            mo.md(f"$\\delta$ = {float(_delta):.3e} ≤ $u = \\tfrac12 10^{{1-p}}$ = {float(_u):.1e} "
                  + ("— изгубени се цифри од помалиот собирок!" if _delta else "— нема загуба.")),
        ])
    except Exception:
        _out = mo.md("⚠️ Внесете валидни броеви.")
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Пример 14 – бинарно собирање во IEEE 754 (единична прецизност)
    Двата броја се прикажуваат како $S\;E\;M$; помалиот собирок се поместува надесно $E_1-E_2$ места
    (скриениот бит влегува во мантисата), се собира, па се нормализира и заокружува.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    b14_a = mo.ui.text(value="0.25", label="a (> 0)")
    b14_b = mo.ui.text(value="100", label="b (> 0)")
    mo.hstack([b14_a, b14_b], justify="start", gap=1.5)
    return b14_a, b14_b


@app.cell(hide_code=True)
def _(b14_a, b14_b, mo, np, struct):
    def _fields(x):
        _b = format(struct.unpack(">I", struct.pack(">f", float(np.float32(x))))[0], "032b")
        return _b[0], int(_b[1:9], 2), int(_b[9:], 2)

    try:
        _xa, _xb = float(b14_a.value), float(b14_b.value)
        assert _xa > 0 and _xb > 0
        _A, _B = sorted([np.float32(_xa), np.float32(_xb)])       # A е помалиот
        _, _Ea, _Ma = _fields(_A)
        _, _Eb, _Mb = _fields(_B)
        assert _Ea > 0 and _Eb > 0
        _sigA, _sigB = (1 << 23) | _Ma, (1 << 23) | _Mb          # 24-битни мантиси со скриен бит
        _d = _Eb - _Ea
        _lines = [
            f"помал  : 0 {_Ea:08b} 1.{_Ma:023b}   = {float(_A)!r}",
            f"поголем: 0 {_Eb:08b} 1.{_Mb:023b}   = {float(_B)!r}",
            "",
            f"E_b − E_a = {_Eb:08b} − {_Ea:08b} = {_d:08b} = ({_d})₁₀ места",
            "",
        ]
        _G = 3  # чуварски бити за прикажување на изгубените бити
        _sa = _sigA << _G
        for _k in range(1, min(_d, 30) + 1):
            _sh = _sa >> _k
            _s = format(_sh, f"0{24 + _G}b")
            _lines.append(f"  0 {_Ea + _k:08b} {_s[0]}.{_s[1:24]}|{_s[24:]}  (поместено {_k})")
        if _d > 30:
            _lines.append(f"  … (вкупно {_d} поместувања – помалиот број целосно „исчезнува“)")
        _shA = (_sigA << _G) >> _d if _d < 64 else 0
        _sumv = (_sigB << _G) + _shA
        _E = _Eb
        if _sumv >= (1 << (24 + _G)):
            _sumv_n, _E = _sumv >> 1, _E + 1
        else:
            _sumv_n = _sumv
        _r = float(np.float32(_A) + np.float32(_B))
        _, _Er, _Mr = _fields(_r)
        _sv = format(_sumv, f"0{25 + _G}b")
        _lines += [
            "",
            "собирање (не заборавајте го скриениот бит!):",
            f"    0 {_Eb:08b} {format(_sigB << _G, f'0{24+_G}b')[0]}.{format(_sigB << _G, f'0{24+_G}b')[1:24]}|{format(_sigB << _G, f'0{24+_G}b')[24:]}",
            f"  + 0 {_Eb:08b} {format(_shA, f'0{24+_G}b')[0]}.{format(_shA, f'0{24+_G}b')[1:24]}|{format(_shA, f'0{24+_G}b')[24:]}",
            "  " + "-" * 44,
            f"    0 {_Eb:08b} {_sv[:-(23+_G)].lstrip('0') or '0'}.{_sv[-(23+_G):-_G]}|{_sv[-_G:]}"
            + ("   ← пренос: мантисата ≥ 2, следи поместување и e+1" if _sv[0] == "1" else ""),
            "",
            "нормализација + заокружување (бити по '|' се отфрлаат):",
            f"    0 {_Er:08b} {_Mr:023b}",
        ]
        _exact = float(_A) + float(_B)
        _out = mo.vstack([
            mo.Html("<pre style='font-size:0.85em'>" + "\n".join(_lines) + "</pre>"),
            mo.md(f"Резултат во float32: **{_r!r}**, точен збир на зачуваните вредности: {_exact!r} "
                  + ("✅ точно" if _r == _exact else f"⚠️ грешка {abs(_r-_exact):.3g} (изгубени бити)")),
        ])
    except Exception:
        _out = mo.md("⚠️ Внесете два позитивни нормализирани броја.")
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Пробајте: `0.25 + 100` (пример од скриптата), `1 + 1e-8` (помалиот исчезнува – $1\cdot10^{-8} < u$),
    `0.1 + 0.2`, `16777216 + 1`.

    ---
    ## Зошто е ова важно за симулациите? 🛰️

    ### (а) Аритметиката не е асоцијативна, и 0.1 + 0.2 ≠ 0.3
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    _a, _b, _c = 1e16, -1e16, 1.0
    _s10 = 0.0
    for _k in range(10):
        _s10 = _s10 + 0.1
    _f32 = np.float32
    mo.md(f"""
    | Израз | Резултат (float64) |
    |---|---|
    | `0.1 + 0.2` | `{0.1 + 0.2!r}` |
    | `0.1 + 0.2 == 0.3` | `{0.1 + 0.2 == 0.3}` |
    | 0.1 собрано 10 пати (`s = s + 0.1`) | `{_s10!r}` |
    | `(1e16 + (-1e16)) + 1` | `{(_a + _b) + _c!r}` |
    | `1e16 + ((-1e16) + 1)` | `{_a + (_b + _c)!r}` |
    | `float32(16777216) + 1` | `{float(_f32(16777216) + _f32(1))!r}` |

    👉 Затоа во код **никогаш** не споредуваме реални броеви со `==`, туку `abs(a - b) < tol`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### (б) Акумулирање на време во симулација: `t = t + Δt`

    Во симулација на ТК систем со фреквенција на примероци $f_s$, времето често се пресметува со $t_{n+1}=t_n+\Delta t$.
    Секое собирање внесува грешка до $u\cdot t$, па грешката **расте** со бројот на чекори.
    Подобро: $t_n = n\cdot\Delta t$ (едно заокружување).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    acc_fs = mo.ui.dropdown(options=["1e3", "1e4", "1e5", "1e6", "1e7"], value="1e5", label="f_s [Hz]")
    acc_N = mo.ui.dropdown(options=["1e4", "1e5", "1e6", "2e6"], value="1e6", label="Број примероци N")
    acc_f0 = mo.ui.dropdown(options=["100", "1000", "10000"], value="1000", label="f₀ на носител [Hz]")
    mo.hstack([acc_fs, acc_N, acc_f0], justify="start", gap=1.5)
    return acc_N, acc_f0, acc_fs


@app.cell(hide_code=True)
def _(acc_N, acc_f0, acc_fs, mo, np, plt):
    _fs, _N, _f0 = float(acc_fs.value), int(float(acc_N.value)), float(acc_f0.value)
    _n = np.arange(_N)
    _t_true = _n / _fs                                   # float64 референца

    _dt32 = np.float32(1 / _fs)
    _t_acc32 = np.concatenate([[0], np.cumsum(np.full(_N - 1, _dt32, dtype=np.float32), dtype=np.float32)])
    _t_mul32 = (_n.astype(np.float32) * _dt32).astype(np.float32)
    _t_acc64 = np.concatenate([[0], np.cumsum(np.full(_N - 1, 1 / _fs))])

    # максимална грешка до моментот t (кумулативен максимум)
    _err_acc32 = np.maximum.accumulate(np.abs(_t_acc32.astype(np.float64) - _t_true))
    _err_mul32 = np.maximum.accumulate(np.abs(_t_mul32.astype(np.float64) - _t_true))
    _err_acc64 = np.maximum.accumulate(np.abs(_t_acc64 - _t_true))

    # фазна грешка на носителот cos(2π f0 t), во степени (над 180° фазата е целосно „изгубена“)
    def _ph(e):
        return np.minimum(np.degrees(2 * np.pi * _f0 * e), 180.0)

    _step = max(1, _N // 4000)
    _tt = _t_true[::_step]
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11, 3.4))
    for _err, _lab in [(_err_acc32, "float32, t += Δt"), (_err_mul32, "float32, t = n·Δt"), (_err_acc64, "float64, t += Δt")]:
        _ax1.semilogy(_tt, np.maximum(_err[::_step], 1e-18), label=_lab)
        _ax2.semilogy(_tt, np.maximum(_ph(_err[::_step]), 1e-12), label=_lab)
    _ax1.set_xlabel("t [s]")
    _ax1.set_title("Максимална грешка во времето t [s]")
    _ax1.legend(fontsize=8)
    _ax2.axhline(1, color="gray", ls=":", lw=1)
    _ax2.set_xlabel("t [s]")
    _ax2.set_ylabel("степени")
    _ax2.set_title(f"Фазна грешка на носител f₀ = {_f0:g} Hz")
    _ax2.legend(fontsize=8)
    _fig.tight_layout()

    def _fmt(v):
        return "≥ 180° (фазата е целосно изгубена)" if v >= 180 else f"{v:.3g}°"

    mo.vstack([
        _fig,
        mo.md(f"""
    На крајот ($t \\approx {_t_true[-1]:.3g}$ s), фазна грешка на носителот:

    - float32, $t \\mathrel{{+}}= \\Delta t$: **{_fmt(_ph(_err_acc32[-1]))}**
    - float32, $t = n\\Delta t$: **{_fmt(_ph(_err_mul32[-1]))}**
    - float64, $t \\mathrel{{+}}= \\Delta t$: **{_fmt(_ph(_err_acc64[-1]))}**

    За кохерентен BPSK приемник фазна грешка од неколку степени веќе видливо го влошува BER –
    грешка која потекнува **само од компјутерската аритметика**, а не од моделираниот систем!
    Кај float32 со акумулирање, кога $t$ ќе порасне доволно, $\\Delta t$ станува помало од половина
    растојание меѓу соседни броеви и $t + \\Delta t = t$ — времето „застанува“.
    """),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### Прашања за самопроверка
    1. Колку позитивни нормализирани броеви има системот β = 2, p = 3, e ∈ [−1, 2]? Проверете со првиот пример.
    2. Зошто 0.25 и 100 се точно претставливи, а 0.1 не е?
    3. Колкава е најголемата релативна грешка ако бројот 3.3 се зачува во float32? А во float64?
    4. Кој е најмалиот позитивен $\varepsilon$ за кој `1 + ε ≠ 1` во float64? (Намиг: поврзете го со $u$.)
    5. Зошто при симулација на 10⁷ примероци е подобро $t_n = n\Delta t$ отколку $t_{n+1}=t_n+\Delta t$?
    """)
    return


if __name__ == "__main__":
    app.run()
