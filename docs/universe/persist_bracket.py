import math

# --- record inputs (SWEEP_hct_model s2.2, s2.5-2.6, s7.1) ---
mu_w = {'low(upper-CI-ish)':0.66,'central':0.118,'high(best)':0.003}   # mean surviving clonogens/dog after whole allo program (OUTCOME)
K_win = {'low':0.65,'central':2.6,'high':4.2}; T_win=166.0
rate_win = {k:v/T_win for k,v in K_win.items()}
print("window net rate /d", {k:round(v,4) for k,v in rate_win.items()})
# --- dog hazard bound after window (8 dogs alive >=4.1 y, 0 events after day 268) ---
for label,start_y in [('after day 180 (0.5 y)',0.5),('after yr 1',1.0),('after yr 2',2.0)]:
    dy = 8*(4.1-start_y)
    ub = 2.9957/dy
    print(f"dog late-hazard upper95 {label}: {dy:.1f} dog-y -> {ub:.3f}/yr")
# --- required persistent net kill kp so that mean residual lineages mu(10y) <= X ---
T10=3650.0
print("\nrequired persistent net kill kp (e-folds/day) so mu(10y)<=X, kp acting from day 166:")
for lab,mu0 in mu_w.items():
    for X in (0.05,0.01,0.001):
        if mu0<=X: print(f"  mu_w {lab} {mu0}: X={X}: already below, kp=0"); continue
        kp = math.log(mu0/X)/(T10-T_win)
        print(f"  mu_w {lab:18s} {mu0:5.3f}: X={X:<6}: kp={kp:.5f}/d = {kp/rate_win['central']*100:.1f}% of central window rate")
# --- human AML late-relapse hazard decline (PMID 38611097, n=376; 142 relapses; 68% in yr1; 26 beyond 2y) ---
n=376; r1=round(0.68*142); r_late=26; r_y2=142-r1-r_late
h1 = -math.log(1-r1/n)
h2 = -math.log(1-r_y2/(n-r1))
print(f"\nAML cohort: yr1 relapses {r1} (cum {r1/n:.3f}), yr2 {r_y2}, >=2y {r_late}")
print(f"crude hazards (ignores competing death): yr1 {h1:.3f}/yr, yr2 {h2:.3f}/yr; decline factor {h1/h2:.1f}; e-fold decline {math.log(h1/h2):.2f}/yr = {math.log(h1/h2)/365:.4f}/d")
at_risk_late = n-r1-r_y2
for fu in (6,8,10):
    h3 = -math.log(1-r_late/at_risk_late)/fu
    print(f"  >=2y late hazard if mean follow-up beyond yr2 = {fu} y: {h3:.4f}/yr; yr2->late decline {h2/h3:.1f}x; e-fold rate over ~{fu/2+1.5:.1f} y: {math.log(h2/h3)/((fu/2+1.5)*365):.4f}/d")
# SFGM-TC: 4.2% of 7582 late (>=2y) vs 33.8% total relapse
print("\nSFGM-TC acute leukaemia: late relapse 4.2% of all vs 33.8% relapse overall -> late share", round(0.042/0.338,3))
# --- sensitivity: e-folds accrued beyond window at fractions of window rate ---
print("\ne-folds accrued by year 4 / year 10 at fraction f of central window rate:")
for f in (0.05,0.1,0.25,0.5,1.0):
    r=f*rate_win['central']
    print(f"  f={f:<4}: kp={r:.5f}/d  y4 {r*(1460-166):.2f}  y10 {r*(3650-166):.2f} e-folds")
# --- hold floor: gross credit needed to prevent regrowth = growth bar ---
g=0.0903
print("\nhold floor: net kill 0 => gross = g =",g,"/d (margin 0: no regrowth, no clearance); window gross central", round(g+rate_win['central'],4))
