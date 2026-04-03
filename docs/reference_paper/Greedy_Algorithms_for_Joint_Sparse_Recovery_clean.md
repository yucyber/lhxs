# Greedy Algorithms for Joint Sparse Recovery

**Authors:** Jeffrey D. Blanchard, Michael Cermak, David Hanle, and Yirong Jing  
**Institution in PDF:** Grinnell College  
**Document type:** research paper PDF converted to Markdown for AI ingestion  
**Original language:** English  
**Source file:** `16  Blanchard 等 - 2014 - Greedy Algorithms for Joint Sparse Recovery - 副本.pdf`

> Notes
> - This is a machine-readable conversion optimized for AI tools and RAG pipelines.
> - Page markers are preserved as HTML comments: `<!-- page: N -->`.
> - Formulas are kept as plain text where possible; some PDF math extraction artifacts may remain.



<!-- page: 1 -->

Greedy Algorithms for Joint Sparse Recovery
Jeffrey D. Blanchard, Michael Cermak, David Hanle, and Yirong Jing, Grinnell College
## Abstract

Five known greedy algorithms designed for the
single measurement vector setting in compressed sensing and
sparse approximation are extended to the multiple measurement
vector scenario: Iterative Hard Thresholding (IHT), Normalized
IHT (NIHT), Hard Thresholding Pursuit (HTP), Normalized
HTP (NHTP), and Compressive Sampling Matching Pursuit
(CoSaMP). Using the asymmetric restricted isometry property
(ARIP), sufficient conditions for all five algorithms establish
bounds on the discrepancy between the algorithms' output and
the optimal row-sparse representation. When the initial multiple
measurement vectors are jointly sparse, ARIP-based guarantees
for exact recovery are also established. The algorithms are then
compared via the recovery phase transition framework. The
strong phase transitions describing the family of Gaussian matrices which satisfy the sufficient conditions are obtained via known
bounds on the ARIP constants. The algorithms' empirical weak
phase transitions are compared for various numbers of multiple
measurement vectors. Finally, the performance of the algorithms
is compared against a known rank aware greedy algorithm, Rank
Aware Simultaneous Orthogonal Matching Pursuit + MUSIC.
Simultaneous recovery variants of NIHT, NHTP, and CoSaMP
all outperform the rank-aware algorithm.
## Keywords

Compressed sensing, greedy algorithms, multiple measurement vectors, joint sparsity, row sparse matrices,
performance comparison
## I. Introduction
### A. Joint Sparse Recovery of Multiple Measurement Vectors
The single measurement vector (SMV) formulation is now
standard in sparse approximation and compressed sensing
literature. For m < n, x ∈Rn, A ∈Rm×n, and y = Ax ∈
Rm, one seeks to recover the signal or vector x from the
measurements y when the linear measurement process defined
by A is known. While this problem is NP-hard in general [1],
if A is chosen wisely and x is sparse, several reconstruction
algorithms are known to guarantee exact recovery of x.
When x is not exactly sparse, but instead has a good sparse
approximation, or when the measurements y are corrupted by
noise, bounds on the recovery error are also known.
A natural extension of this problem is the multiple measurement vector (MMV) problem where a single matrix A
is utilized to obtain measurements of multiple signals: y1 =
Ax1, y2 = Ax2, . . . , yl = Axl. Rather than recovering the
l signals separately, one attempts to simultaneously recover
all l signals from the matrix formulation Y = AX where
X = [x1|x2| · · · |xl] and thus Y = [y1|y2| · · · |yl]. When the
target signals, {xi}l
i=1, are all predominantly supported on a
Copyright (c) 2013 IEEE. Personal use of this material is permitted.
However, permission to use this material for any other purposes must be
obtained from the IEEE by sending a request to pubs-permissions@ieee.org.
This work was supported by grant NSF DMS 11126152 and the Grinnell
College MAP program. The authors are with the Department of Mathematics
and Statistics, Grinnell College, Grinnell, IA 50112.
Manuscript submitted July 2013; accepted January 2014.
common support set, this approach can lead to a computational
advantage [2], [3]. If the cost per iteration of one run of the
simultaneous recovery algorithm is no worse than l runs of an
equivalent SMV algorithm, the common support set provides
more information to the simultaneous recovery algorithm than
running l independent instances of an SMV algorithm.
### B. Prior Art and Contributions
Beginning with Leviatan, Lutoborski, and Temlyakov [4],
[5], [6], a substantial body of work has been developed
for the MMV problem including [7], [8], [9], [10], [11],
[12], [13], [14]. The majority of the literature focuses on
relaxations, mixed matrix norm techniques, and variants of
orthogonal matching pursuit. Tropp et al. [3], [15] introduced
simultaneous recovery algorithms based on Orthogonal Matching Pursuit (OMP) and convex relaxation. For the greedy
algorithm, Simultaneous OMP (SOMP), Tropp et al. stated
that the analysis of the MMV recovery algorithm permitted
a straightforward extension of the analysis from the SMV
setting. Foucart applied these "capitalization" techniques to
Hard Thresholding Pursuit (HTP) to extend that algorithm to
the MMV setting [2], [16].
In this article, we provide a comprehensive investigation
of the extension to the MMV problem of five known greedy
algorithms designed for the SMV setting: Iterative Hard
Thresholding (IHT) [17], Normalized IHT (NIHT) [18], Hard
Thresholding Pursuit (HTP) [16], Normalized HTP (NHTP)
[16], and Compressive Sampling Matching Pursuit (CoSaMP)
[19]. The article includes:
- a description of the simultaneous joint sparse recovery
algorithms (Section II-B);
- sufficient conditions based on the asymmetric restricted
isometry property which guarantee joint sparse recovery
and bound recovery error for joint sparse approximation
(Section II-C);
- a quantitative comparison of the theoretical sufficient
conditions through the strong recovery phase transition
framework (Section III-A);
- an empirical, average case performance comparison
through the weak recovery phase transition framework
(Section III-B);
- an
empirical,
average
case
performance
comparison
against
a
known
rank-aware
algorithm
RASOMP+MUSIC (Section III-C).
The MMV algorithms Simultaneous IHT (SIHT), Simultaneous NIHT (SNIHT), Simultaneous HTP (SHTP)1, Simultaneous NHTP (SNHTP), and Simultaneous CoSaMP
(SCoSaMP) are natural extensions of the well-known SMV
1This algorithm and its associated convergence guarantee were originally
presented by Foucart [2]



<!-- page: 2 -->

versions of the algorithms and reduce to the SMV versions
when applied to the measurements of a single sparse vector.
While the analysis closely follows the MMV extension techniques of Tropp et al. [3], [15] and the proofs closely follow
the analysis of Foucart for the SMV versions of the algorithms
[20], the convergence analysis provides three generalizations.
The results are written in terms of the asymmetric restricted
isometry constants [21] thereby providing weaker sufficient
conditions than those derived with the standard, symmetric
restricted isometry constants. Since empirical testing [22]
suggests tuning the step size in SIHT and SHTP according
to family from which A is drawn, the analysis permits an
arbitrary fixed step size between 0 and 1. Finally, the results
for the normalized algorithms NIHT and NHTP are stated
explicitly.
These sufficient conditions are quantitatively compared by
employing the techniques for the strong recovery phase transition framework of [21], [23]. The strong phase transitions
associated with the sufficient conditions identify two important
facts. First, simpler algorithms often admit a simpler analysis
which yield more relaxed sufficient conditions even though the
algorithms may have inferior observed performance. Second,
the sufficient conditions obtained via the restricted isometry
property are exceedingly pessimistic and apply to a regime
of problems unlikely to be realized in practice. While critical
to understanding the theoretical behavior of the algorithms,
the pessimistic, worst-case sufficient conditions fail to inform
practitioners about typical algorithm behavior. From this point
of view, the empirical average-case performance comparisons
provide the most important information for selecting an algorithm for application.
### C. Organization
The algorithms are detailed in Section II-B with the joint
sparse recovery guarantees provided in Section II-C. In Section III-A, the theoretical sufficient conditions for each of
the algorithms are compared via the strong phase transition
framework [21], [23]. In Section III-B, the average case
performance of the algorithms is then compared via empirical
weak recovery phase transitions similar to other empirical
studies [22], [24]. In Section III-C the typical performance
of these "rank blind" algorithms is then juxtaposed with
the performance of the "rank aware" greedy algorithm Rank
Aware SOMP + MUSIC [9], [25], [12].
As the convergence analysis leading to Theorem 1 closely
follows the techniques of Foucart [20], a representative proof
for SIHT and SNHTP is provided in Appendix A. For completeness, all omitted proofs are available in the supplementary
material [26]. The supplementary material also includes the
analysis required to employ the strong phase transition techniques of [23] and additional empirical performance comparisons with measurements obtained from randomly subsampled
discrete cosine transforms.
## II. Recovery Guarantees
### A. Notation
Let M(r, c) denote the set of matrices with r rows and c
columns with entries drawn from R or C. If X is a collection
of l vectors in Rn or Cn, then X ∈M(n, l) and we let X(i)
denote the ith row of X while Xi represents the ith column.
Let S ⊂{1, . . . , n} be an index set and define X(S) as the
matrix X restricted to the rows indexed by this set; in other
words, the entries in the rows indexed by S remain unchanged
while all other rows of X(S) have all entries set to 0. The linear
measurement process is defined by a matrix A ∈M(m, n) and
the restriction AS represents the sub-matrix of A obtained by
selecting the columns of A indexed by S. A∗denotes the
conjugate transpose of A.
Throughout the manuscript, the row support, or simply
support, of a matrix Z ∈M(n, l) is the index set of rows
which contain nonzero entries. Thus, when X is a collection
of l column vectors, X = [X1|X2| . . . |Xl], we have
supp(X) =
l[
i=1
supp(Xi).
The matrix X is k-row sparse (or the set {Xi : i = 1, . . . , l}
is jointly k-sparse) if |supp(X)| ≤k. In particular, if |S| is the
cardinality of the index set S, then X(S) is |S|-row sparse. Let
χn,l(k) ⊂M(n, l) be the subset of k-row sparse n×l matrices;
the set of k-sparse column vectors will be abbreviated χn(k).
The MMV sparse approximation problem is equivalent to
constructing a row sparse approximation of a matrix X from
the measurements Y = AX. Consider first the ideal case of
measuring a k-row sparse matrix X ∈χn,l(k) where T =
supp(X). Given the measurements Y = AX ∈M(m, l), the
task is to exactly recover the k-row sparse matrix X = X(T ).
This is equivalent to simultaneously recovering l jointly ksparse vectors. This ideal setting of attempting to recover
a perfectly row sparse matrix from clean measurements is
unlikely to present itself in applications. Instead, the task
will be to find an accurate row sparse approximation to a
matrix X ∈M(n, l). Suppose T is the index set of rows of
X ∈M(n, l) which have the k largest row-ℓ2-norms, and the
measurement process is corrupted by additive noise, namely
Y = AX + E for some noise matrix E ∈M(m, l). The
row sparse approximation problem seeks an approximation to
X(T ). The recovery guarantees are presented in terms of the
Frobenius norm of the discrepancy between the algorithms'
output ˆX and the optimal k-row sparse approximation X(T ).
The Frobenius norm of a matrix X ∈M(n, l) is defined by
∥X∥2
F =
l
X
j=1
∥Xj∥2
2 =
l
X
j=1
n
X
i=1
|Xi,j|2 .
### B. Greedy MMV Algorithms
To solve the MMV or row sparse approximation problem,
we propose the extension of five popular greedy algorithms
designed for the SMV problem: IHT, NIHT, HTP, NHTP,
and CoSaMP. Each of these algorithms is a support identification algorithm. The simultaneous recovery algorithms,
prefixed with the letter S, are defined in Algorithms 1-3. Each
algorithm follows the same initialization procedure. The initial
approximation matrix is the zero matrix X0 = 0 and thus the
initial residual is the matrix of input measurements R0 = Y .
When an initial proxy for the support set is needed, T 0 =



<!-- page: 3 -->

DetectSupport(A∗Y, k) where DetectSupport(Z, s)
is a subroutine identifying the index set of the rows of Z
with the s largest row-ℓ2-norms. In Algorithms 1 and 3, the
thresholding operator Threshold(Z, S) restricts the matrix
Z to the row index set S, i.e. Z(S) = Threshold(Z, S).
The choice of stopping criteria plays an important role for
the algorithms, and the stopping criteria employed for the
empirical testing are outlined in Section III-B.
### Algorithm 1: SIHT / SNIHT
1: for iteration j until stopping criteria do
2:
if (SIHT) then
3:
ωj = ω
4:
else if (SNIHT) then
5:
ωj =
∥(A∗Rj-1)(T j-1)∥2
F
∥AT j-1(A∗Rj-1)(T j-1)∥2
F
6:
end if
7:
Xj = Xj-1 + ωj  A∗Rj-1
8:
T j = DetectSupport(Xj, k)
9:
Xj = Threshold(Xj, T j)
10:
Rj = Y -AXj
11: end for
12: return
ˆX = Xj⋆when stopping at iteration j⋆.
### Algorithm 2: SHTP / SNHTP
1: for iteration j until stopping criteria do
2:
if (SHTP) then
3:
ωj = ω
4:
else if (SNHTP) then
5:
ωj =
∥(A∗Rj-1)(T j-1)∥2
F
∥AT j-1(A∗Rj-1)(T j-1)∥2
F
6:
end if
7:
Xj = Xj-1 + ωj  A∗Rj-1
8:
T j = DetectSupport(Xj, k)
9:
Xj = arg min{∥Y -AZ∥F : supp(Z) ⊆T j}
10:
Rj = Y -AXj
11: end for
12: return
ˆX = Xj⋆when stopping at iteration j⋆.
In iteration j, SIHT and SHTP update the previous approximation Xj-1 by taking a step of predefined, fixed length ω
in the steepest descent direction A∗Rj-1. A new proxy for
the support set, T j, is then obtained by selecting the rows
of Xj with greatest row-ℓ2-norms. The two algorithms differ
in how the support proxy T j is utilized: SIHT employs a
hard thresholding operator which restricts the approximation
Xj to the rows indexed by T j while SHTP projects the
measurements Y onto the support set T j.
The normalized variants of these two algorithms, SNIHT
and SNHTP, proceed in a nearly identical fashion although
the potentially inaccurate fixed step size is replaced by a nearoptimal step size ωj. If T j = T j-1 and T j contains the
support set T of the measured row-sparse matrix X = X(T ),
the normalized step-size
ωj =
∥(A∗Rj-1)(T j-1)∥2
F
∥AT j-1(A∗Rj-1)(T j-1)∥2
F
is optimal in terms of minimizing the norm of the residual
Rj. When elements of the support T of the measured matrix
X = X(T ) are missing from the current support proxy T j,
the step-size is nearly optimal in the sense that the unknown
error in the step size is exclusively determined by the missing
elements T\T j. In other words, when considering minimizing
the norm of the residual
Rj = Y -AX(T j) = A(X(T ) -X(T j)),
the optimal step size is not computable without oracle information regarding the new support proxy T j and the support
T of the target matrix X = X(T ).
### Algorithm 3: SCoSaMP
1: for iteration j until stopping criteria do
2:
Sj = DetectSupport(A∗Rj-1, 2k)
3:
Qj = T j-1 ∪Sj
4:
U j = arg min{∥Y -AZ∥F : supp(Z) ⊆Qj}
5:
T j = DetectSupport(U j, k)
6:
Xj = Threshold(U j, T j)
7:
Rj = Y -AXj
8: end for
9: return
ˆX = Xj⋆when stopping at iteration j⋆.
SCoSaMP is also a support identification algorithm but
takes a fundamentally different approach to constructing the
approximation Xj. The support of the previous approximation
T j-1 is combined with the set of 2k indices of the largest row-
ℓ2-norms of the residual A∗Rj-1. This larger set, Qj, has at
most 3k indices and the next approximation is determined
by projecting the measurements Y onto this subspace. The
best k-row-sparse approximation is then obtained by hard
thresholding this projection to the rows with k largest row-
ℓ2-norms.
### C. Sufficient Restricted Isometry Properties
The following recovery guarantees are based on the restricted isometry property (RIP) introduced by Cand´es and
Tao [27]. The standard RIP constant of order k is the smallest
value Rk such that
(1 -Rk)∥x∥2
2 ≤∥Ax∥2
2 ≤(1 + Rk)∥x∥2
2
for all x ∈χn(k). The RIP constants are clearly determined
by the most extreme singular values of all m × k submatrices
of A formed by selecting k columns. However, the smallest
and largest singular values of the submatrices can deviate from
1 in a highly asymmetric fashion since the smallest singular
values are nonnegative while the largest singular values can
be much greater than 1. Therefore, it is beneficial to treat the
sets of smallest and largest singular values independently. A
natural relaxation of the standard RIP constants is to use an
asymmetric version of Cand´es and Tao's RIP constants; the
asymmetric RIP constants presented in [21] capture the most
extreme smallest and largest singular values from the set of
all m × k matrices formed by selecting k columns of A.



<!-- page: 4 -->

alg
ARIP Condition
µalg(k; A)
ξalg(k; A)
SIHT
2φω(3k) < 1
2φω(3k)
2ω√1 + U2k
SNIHT
2U3k + 2L3k + Lk < 1
2ψ(3k)
2
 √
1+U2k
1-Lk

SHTP
√
3φω(3k) < 1
r
2[φω(3k)]2
1-[φω(2k)]2
q
2(1+U2k)
1-[φω(2k)]2 +
√
1+Uk
(1-Lk)(1-φω(2k))
SNHTP
√
3U3k +
√
3L3k + Lk < 1
r
2[ψ(3k)]2
1-[ψ(2k)]2
q
2(1+U2k)
1-[ψ(2k)]2 +
√
1+Uk
(1-Lk)(1-ψ(2k))
SCoSaMP
q
5+
√
73
2
max{U4k, L4k} < 1
r
4[R4k]2(1+3[R4k]2)
1-[R4k]2
p
3(1 + U3k) +
p
1 + 3[R4k]2
q
2(1+U4k)
1-[R4k]2 +
q
1+U3k
1-R4k

**TABLE I**
SUFFICIENT ARIP CONDITONS WITH CONVERGENCE FACTORS µalg(k; A) AND STABILITY FACTORS ξalg(k; A) FOR ALGS. 1-3. LET
φω(ck) = max{|1 -ω(1 + Uck)|, |1 -ω(1 -Lck)|} AND ψ(ck) = Uck+Lck
1-Lk
FOR THE ARIP CONSTANTS Lk, Lck, AND Uck OF THE m × n MATRIX A.
**Definition 1 (RIP Constants). For A ∈M(m, n), the lower**
and upper asymmetric restricted isometry property (ARIP)
constants of order k are denoted Lk and Uk, respectively, and
are defined as:
Lk := min
c≥0 c subject to
(
(1 -c)∥x∥2
2 ≤∥Ax∥2
2
for all x ∈χn(k)
(1)
Uk := min
c≥0 c subject to
(
(1 + c)∥x∥2
2 ≥∥Ax∥2
2
for all x ∈χn(k)
(2)
The standard (symmetric) restricted isometry property (RIP)
constant of order k is denoted Rk and can be defined in terms
of the ARIP constants:
Rk := max{Lk, Uk}.
(3)
The main result for each of the algorithms takes on the
same formulation. Therefore, we consolidate the results into a
single theorem where the sufficient ARIP conditions are stated
in Table I along with the appropriate convergence and stability
factors. Theorem 1 provides a bound on the discrepancy of the
row sparse approximation obtained by the greedy algorithms
and the optimal row sparse approximation.
**Theorem 1 (Simultaneous Sparse Approximation). Suppose**
A ∈M(m, n), X ∈M(n, l), T is the index set of rows of X
with the k largest row-ℓ2-norms, Y = AX +E = AX(T ) + ˜E
for some error matrix E and ˜E = AX(T c) + E. Assume
the initial approximation is the zero matrix X0 = 0. If
A satisfies the sufficient ARIP conditions stated in Table I,
then each algorithm, alg from {SIHT, SNIHT, SHTP, SNHTP,
SCoSaMP}, is guaranteed after j iterations to return an
approximation Xj satisfying
∥Xj -X(T )∥F ≤
 µalgj ∥X(T )∥F +
ξalg
1 -µalg ∥˜E∥F ;
(4)
where µalg ≡µalg(k; A) and ξalg ≡ξalg(k; A) are defined in
Table I.
In the ideal, exact row sparse setting, a more specific result
applies. Under the same sufficient ARIP conditions the greedy
algorithms are all guaranteed to converge to the targeted row
sparse matrix and the support set is identified in a finite number
of iterations.
**Corollary 1 (Simultaneous Exact Recovery). Suppose A ∈**
M(m, n), X ∈χn,l(k), Y = AX, and the initial approximation is the zero matrix X0 = 0. If A satisfies the sufficient
ARIP conditions stated in Table I, then each algorithm, alg
from {SIHT, SNIHT, SHTP, SNHTP, SCoSaMP}, is guaranteed
after j iterations to return an approximation Xj satisfying
∥Xj -X∥F ≤
 µalgj ∥X∥F ,
(5)
where µalg ≡µalg(k; A) is defined in Table I.
Moreover, define
jalg
max =
 log νmin(X)
log µalg(k; A)

+ 1
(6)
where
νmin(X) = mini∈supp(X) ∥X(i)∥2
∥X∥F
.
Then, if j ≥jalg
max, supp(Xj) ⊂supp(X).
The ARIP analyses of the MMV variants of the greedy
algorithms are clearly independent of the number of vectors (columns) contained in X, and the sufficient conditions
therefore apply to the SMV case. Hence the sufficient ARIP
conditions in Table I capture the known conditions for the
SMV case presented by Foucart [20] namely R3k < 1/2
for IHT, R3k < 1/
√
3 for HTP, and R4k <
q
2/(5 +
√
73)
for CoSaMP. The standard RIP extensions to the normalized
versions are therefore R3k < 1/5 for NIHT and R3k <
1/(2
√
3 + 1) for NHTP. The proofs of Theorem 1 and
**Corollary 1 appear in Appendix A and [26].**
## III. Algorithm Comparison
### A. Strong Phase Transitions
The comparison of sufficient conditions based on restricted
isometry properties can be challenging when the conditions
do not take on the same formulation or use different support
sizes for the RIP constants. Blanchard, Cartis, and Tanner
[21] developed bounds on the ARIP constants for Gaussian
matrices which permit a quantitative comparison of sufficient
ARIP conditions via the phase transition framework. The unit
square defines a phase space for the ARIP conditions under a
proportional growth asymptotic, namely (m/n, k/m) →(δ, ρ)
as m →∞for (δ, ρ) ∈[0, 1]2. Utilizing the bounds on the
ARIP constants it is possible to identify lower bounds on



<!-- page: 5 -->

0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
0.5
1
1.5
2
2.5
x 10
-3
← SIHT
← SNIHT
← SHTP
← SNHTP
← SCoSaMP
ρ=k/m
δ=m/n
Strong Recovery Phase Transitions: µalg(δ,ρ)=1
Fig. 1.
Lower bounds on the strong recovery phase transition curves for
SIHT, SNIHT, SHTP, SNHTP, and SCoSaMP. Beneath the line, the associated
sufficient condition from Table I is satisfied with overwhelming probability on
the draw of A from the Gaussian matrix ensemble; therefore µalg(k; A) < 1.
strong phase transition curves ρalg
S (δ) which delineate a region
k/m = ρ < ρalg
S (δ) where the sufficient ARIP condition is
satisfied with overwhelming probability on the draw of A from
the Gaussian ensemble, i.e. the entries of A are drawn i.i.d.
from the normal distribution N(0, m-1). For a more general
description of the phase transition framework in the context
of compressed sensing, see [28].
For each algorithm, the strong phase transition curve ρalg
S (δ)
is the solution to the equation µalg(δ, ρ) ≡1 where µalg(δ, ρ)
is obtained by replacing the ARIP constants in µalg(k; A)
by their respective probabilistic bounds from [21]. A higher
strong phase transition curve indicates a sufficient condition
which is satisfied by a larger family of Gaussian matrices
since the region below the curves ρalg
S (δ) demonstrate that
µalg(k, A) < 1 with overwhelming probability. Figure 1
shows that SHTP (with ω = 1) has the best sufficient ARIP
condition among these five algorithms while the efficacy of the
conditions for the remaining algorithms from largest region
of the phase space to smallest is SIHT, SCoSaMP, SNHTP,
SNIHT.
When l = 1, the simultaneous recovery algorithms are
identical to their SMV variants. Moreover, the sufficient conditions in Table I are independent of the number of multiple
measurement vectors and therefore apply directly to the SMV
algorithms. A similar analysis for SMV greedy algorithms was
performed in [23]. Figure 1 shows the lower bound on the
strong phase transition for the five algorithms. The improved
analysis leading to the sufficient conditions in Table I yields
phase transition curves for IHT and CoSaMP that capture
a larger region of the phase space then the phase transition
curves reported in [23]. The strong phase transition curves for
the sufficient ARIP conditions for NIHT, HTP, and NHTP are
reported for the first time.
The lower bounds on the strong phase transition curves
point out the pessimism in the worst case analysis. Notice
that Figure 1 implies the sufficient conditions from Theorem 1
require ρ = k/m < .0008 for SCoSaMP, SNIHT, and SHTP.
The bounds on the ARIP constants are surprisingly tight
and improved bounds by Bah and Tanner [29] show that
the curves defined by the functions ρalg
S (δ) closely identify
the regions of the phase space in which one can expect to
satisfy the sufficient conditions. As shown in [23], empirical
identifications of RIP constants show upper bounds on these
phase transition curves are no more than twice as high as
those depicted in Figure 1. The analysis required to employ the
techniques outlined in [23] is contained in the supplementary
material for this paper [26] along with the phase transition
representation of the stability factors
ξalg
1-µalg from Theorem 1.
### B. Weak Phase Transitions
It is often more useful to understand the average case performance of the algorithms rather than the worst case guarantees
provided by the sufficient conditions and delineated by the
strong phase transition curves of Section III-A. In this section,
we provide empirical average case performance comparisons
via a weak recovery phase transition framework. Although
empirical testing has its limitations, the results presented
here provide insight into the expected relative performance of
the greedy simultaneous sparse recovery algorithms SNIHT,
SNHTP, and SCoSaMP.
The empirical testing was performed using an MMV extension of the Matlab version of the software GAGA for
Compressed Sensing [30], [31]. The setup and procedures are
similar to those outlined in [24]. A random problem instance
consists of generating a random matrix A ∈M(m, n) and a
random MMV matrix X ∈χn,l(k), forming the measurements
Y
= AX, and passing to each algorithm the information
(Y, A, k). To form the MMV matrix X, a row support set
T with |T| = k is chosen randomly and the entries of the
multiple measurement vectors are selected from {-1, 1} with
probability 1/2, thereby forming the matrix X = X(T ) ∈
χn,l(k).
For the results presented here, n = 1024 with tests conducted for 15 values of m where m = ⌈δ · n⌉for
δ ∈{0.01, 0.02, 0.04, 0.06, 0.08, 0.1, . . . , 0.99}
with 8 additional, linearly spaced values of δ from 0.1 to
0.99. For each (m, n) pair, a binary search determines an
interval [kmin, kmax] where the algorithm is observed to have
successfully recovered 8 of 10 trials at kmin and 2 of 10 trials
at kmax. The interval [kmin, kmax] is then sampled with 50
independent, linearly spaced values of k from kmin to kmax,
or every value of k ∈[kmin, kmax] if kmax -kmin ≤50.
Ten tests are conducted for each of the sampled values of
k ∈[kmin, kmax].
The matrix X is determined to be successfully recovered if
the output of the algorithm, ˆX, satisfies
∥ˆX -X(T )∥F ≤0.001.
The empirical weak phase transitions are defined by a logistic
regression of the data which determines a curve ρalg
W (δ) in the
phase space identifying the location of 50% success. For a
detailed explanation of the logistic regression, see [24].
For computational efficiency, the algorithms have been
altered slightly in the testing regime. The projection steps
in Algorithms 2 and 3 have been replaced with a subspace
restricted conjugate gradient projection (see [30]). Empirically,



<!-- page: 6 -->

SCoSaMP has improved performance when the index set Sj
in Step 2 has k entries rather than 2k entries; this change was
implemented in the testing.
Critically important to the empirical testing is establishing
suitable stopping criteria for the greedy algorithms. Following
the extensive work presented in [24], [30], the algorithms
continue to iterate until one of the following stopping criteria
is met:
- the residual is small: ∥Rj∥F < 0.001 · m
n ;
- a maximum number of iterations has been met: 5000 for
### Algorithm 1: and 300 for Algorithms 2 and 3;
- the algorithm is diverging: ∥Rj∥F > 100 · ∥Y ∥F ;
- the residual has failed to change significantly in 16
iterations:
max
i=1,...,16

∥Rj-i+1∥F -∥Rj-i∥F

 < 10-6;
- after many iterations, the convergence rate is close to one:
let c=700 for Algorithm 1 and c=125 for Algorithms 2
and 3,
if j > c and
∥Rj-15∥2
F
∥Rj∥2
F
 1
15
> 0.999.
When any one of the stopping criteria is met at iteration j,
the algorithm terminates and returns the k-row sparse matrix
ˆX = Xj.
As in Section III-A, a higher empirical weak recovery
phase transition curve indicates that the algorithm successfully
recovers a larger set of MMV matrices X. All results presented
in this section have the nonzero entries of the MMV matrix
X selected with equal probability from {-1, 1}; alternative
MMV matrix ensembles, for example selecting the nonzeros
from N(0, 1), result in higher weak phase transition curves.
These findings are consistent with other empirical studies
[22], [24]. Also, throughout this section, the matrix A is
selected from the Gaussian ensemble with entries drawn i.i.d.
from N(0, m-1) for consistency with the strong recovery
phase transition curves from Section III-A. The weak phase
transition curves are higher when the matrix A is constructed
by randomly selecting m rows of the discrete cosine transform;
the empirical results for the DCT matrix ensemble are included
in the supplementary material [26].
To demonstrate the improved performance of the algorithms
from the SMV setting (l = 1) to the MMV setting, the
weak phase transition curves are presented for l = 1, 2, 5, 10.
In Section III-B1, the optimal step size selection in SNIHT
and SNHTP is shown to provide a noticeable advantage over
the fixed step size variants SIHT and SHTP, particularly as
the number of multiple measurement vectors increases. The
performance gain in the exact sparsity MMV setting is detailed
in Section III-B2.
1) Optimal Step Size Selection: The fixed step size in
SIHT and SHTP permits simplified analyses leading to weaker
sufficient conditions than for the optimal step size variants
SNIHT and SNHTP. This is clear from the strong phase
transitions presented in Figure 1. Intuitively, selecting the step
size to minimize the residual in the subspace restricted steepest
descent direction should lead to improved performance. For
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← SNHTP l = 1
← SHTP l = 1
← SNHTP l = 10
← SHTP l = 10
Recovery Phase Transitions: SNHTP vs. SHTP, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← SNIHT l = 1
← SIHT l = 1
← SNIHT l = 10
← SIHT l = 10
Recovery Phase Transitions: SNIHT vs. SIHT, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(a)
(b)
Fig. 2.
Empirical weak recovery phase transitions: fixed versus optimal
step size with A from the Gaussian matrix ensemble. SHTP (ω = 1) versus
SNHTP (a), SIHT (ω = 1) versus SNIHT (b).
the SMV setting, the introduction of the optimal step size
in NIHT provides a significant improvement in average case
performance [18], [24] even when compared to the tuned step
size ω = .65 identified for Gaussian matrices A in [22].
Interestingly, the improvement in the recovery phase transition
for l = 1 is not nearly as dramatic for NHTP compared to HTP
with ω = 1.
In Figure 2, we see that for both SNIHT and SNHTP
(Algorithms 1 and 2), the inclusion of the optimal step size
improves performance in the MMV setting, and the advantage
increases as the number of multiple measurement vectors
increases. Although the analysis is simplified with a fixed
step size, the improved empirical performance suggests that
implementations should utilize the optimal step size, especially
in the MMV setting. When A is a subsampled DCT matrix,
SNIHT and SNHTP are more efficient than the fixed step
size variants, especially in the most interesting regime for
compressing sensing with m/n →0. The comparisons of
the associated weak phase transitions for the DCT matrix
ensembles are displayed in [26, Figure 6].
2) Exact Recovery: Figure 3 shows the empirical weak
recovery phase transition curves ρalg
W (δ) for X ∈χn,l(k) with
n = 1024 and l = 1, 2, 5, 10 for SNIHT, SHTP, and SCoSaMP.
A theoretical average case analysis for the greedy algorithms
considered here is currently unavailable in the literature as
the lack of Lipschitz continuity for the thresholding operation imposes a significant impediment. For the SMV setting,
Donoho and Tanner utilized stochastic geometry to identify
the weak phase transition for recovering a sparse vector via
ℓ1-minimization when A is Gaussian [32], [33]. For reference,
the theoretical weak phase transition for ℓ1-minimization with
l = 1 is included as the blue, dashed curve in Figures 3(a)-(c).
Clearly, each of the algorithms takes advantage of additional
information about the support set provided by the jointly
sparse multiple measurement vectors. As l increases, the
weak phase transitions increase for all three algorithms in
Figure 3. For direct performance comparison, Figure 3(d)
displays the empirical weak recovery phase transition curves
for all three algorithms with l = 2, 10. SNIHT and SNHTP
have very similar weak phase transition curves in the MMV
setting, extending the similar observation for the SMV case
detailed in [24]. When A is Gaussian, SCoSaMP recovers row



<!-- page: 7 -->

0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SNHTP, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SNIHT, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(a)
(b)
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SCoSaMP, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
SCoSaMP l = 2 →
SCoSaMP l = 10 →
← SNHTP l = 2
← SNHTP l = 10
← SNIHT l = 2
← SNIHT l = 10
Recovery Phase Transitions: Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(c)
(d)
*Fig. 3. Empirical weak recovery phase transitions for joint sparsity levels l =*
1, 2, 5, 10 with A from the Gaussian matrix ensemble: SNHTP (a); SNIHT
(b); SCoSaMP (c); All algorithms (d). Theoretical weak phase transition for
ℓ1-minimization is the blue, dashed curve in (a)-(c).
alg
Matrix Ensemble
l = 2
l = 5
l = 10
SNIHT
Gaussian
1.42
1.89
2.09
DCT
1.33
1.74
1.88
SNHTP
Gaussian
1.38
1.83
2.03
DCT
1.31
1.71
1.87
SCoSaMP
Gaussian
1.40
1.92
2.10
DCT
1.38
1.82
1.98
**TABLE II**
THE RATIO OF THE AREA OF THE RECOVERY REGION FOR l = 2, 5, 10
COMPARED TO THE AREA OF THE SINGLE MEASUREMENT VECTOR
RECOVERY REGION.
sparse matrices X for noticeably larger values of ρ = k/m
throughout the phase space, especially as m/n →1, and for
all four values l ∈{1, 2, 5, 10} (l = 1, 5 are omitted from
the plot for clarity). However, when A is a subsampled DCT
matrix, the advantage shown by SCoSaMP is removed. Similar
plots for the subsampled DCT are given in [26].
Referring to the area below the empirical weak phase transition curves as the recovery region, Table II provides the ratio
of the areas of the recovery regions for l = 2, 5, 10 compared
to the area of the recovery region for the SMV setting (l = 1).
When A is drawn from the Gaussian matrix ensemble, the area
of the recovery regions for all three algorithms more than
doubles when 10 jointly sparse vectors are simultaneously
recovered. For l = 10, the area of the recovery region for
SCoSaMP is approximately 1.3 times larger than the area of
the recovery region for SNHTP; see Figure 3(d).
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← SNHTP l = 1
← RASOMP+ l = 1
← SNIHT l = 1
SCoSaMP l = 1 →
← SNHTP l = 10
← RASOMP+ l = 10
← SNIHT l = 10
SCoSaMP l = 10 →
Recovery Phase Transitions: Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
Fig. 4.
Weak Recovery Phase Transitions for Algorithms 1-3 and RASOMP+MUSIC with joint sparsity levels l = 1, 10 with A from the Gaussian
matrix ensemble.
### C. Comparison to Rank Aware Algorithms
Most greedy simultaneous recovery algorithms, including
Algorithms 1-3, fail to incorporate the rank of X in the
algorithms' definition and analysis. From this point of view,
the algorithms are "rank blind". In fact, the ARIP analysis presented here and elsewhere requires the number of observations
(rows of A) to satisfy m ≳Ck log(n) for a constant C. Davies
and Eldar analyzed "rank aware" (RA) greedy algorithms for
the MMV problem [9] which incorporate an orthogonalization
of the column space of the residual in each iteration. Blanchard
and Davies [25] and Lee, Bressler, and Junge [12] considered
rank aware greedy algorithms followed by an application of
MUSIC [34] for incorporating rank awareness in the MMV
setting. For A Gaussian, Blanchard and Davies established that
the logarithmic term in the requisite number of measurements
is reduced by the rank so that m ≳Ck
  1
r log(n) + 1

[25].
Interestingly, Figure 4 shows the seemingly rank blind
greedy algorithms presented here have superior weak phase
transitions than the rank aware algorithm RA-SOMP+MUSIC.
This empirical observation suggests that SNIHT, SNHTP, and
SCoSaMP are somehow rank aware2 and calls for further
exploration. One possible explanation is that when selecting
support sets based on the largest row-ℓ2-norms of the residual
or the current approximation, the DetectSupport step
in Algorithms 1-3 is inherently rank aware providing the
performance gain with the increase in the number of multiple
measurement vectors.
## IV. Conclusion
Five greedy algorithms designed for the SMV sparse approximation problem have been extended to the MMV problem with ARIP guarantees on the approximation errors and
convergence for the ideal exact row sparse situations. The
sufficient ARIP conditions for the algorithms have been compared via the strong phase transition framework for Gaussian
matrices providing the best available strong recovery phase
transitions curves. The importance of the optimal step size
selection in the normalized variants of the algorithms was
2An alternative interpretation is that rank awareness in OMP based algorithms is insufficient to close the performance gap on these more sophisticated
greedy algorithms.



<!-- page: 8 -->

shown through empirical testing to provide a more significant
advantage in the MMV setting than in the SMV setting.
Also, through empirical testing, an average case performance
comparison of the algorithms was presented through the weak
phase transition framework. These greedy algorithms appear
to outperform an explicitly rank aware algorithm.
In this work, we have identified the location of the weak
phase transition curves. Future empirical investigations on
additional performance characteristics for more realistic sized
problems and noisy signals, similar to [24], will better inform
algorithm selection in regions below the weak phase transition
curves for multiple algorithms.
## Appendix A
PROOFS OF RECOVERY GUARANTEES
All inner products in this manuscript are Frobenius matrix
inner products. For Z, W ∈M(r, c), the Frobenius matrix
inner product is defined by
⟨Z, W⟩= trace(W T Z).
The Frobenius norm defined in Section I can be equivalently
defined via the Frobenius matrix inner product: for Z ∈
M(r, c),
∥Z∥2
F = ⟨Z, Z⟩.
### A. Technical Lemmas
The straightforward proofs of Lemmas 1-2 are available in
the supplementary material [26] for completeness.
**Lemma 1. Let Z ∈M(n, l) and let S, T ⊂{1, 2, . . . , n} be**
row index sets with |S| = |T| = k. If T is the index set of the
rows of Z with the k largest row-ℓ2-norms, then
∥Z -Z(T )∥F ≤∥Z -Z(S)∥F .
(7)
**Lemma 2. Suppose Y = AX + E, T = supp(X), and ˜E =**
AX(T c) + E. Let alg be any algorithm from Algorithms 1-3
and let Xj denote the approximation in iteration j from alg.
If there exist nonnegative constants µalg and ξalg such that
µalg < 1 and for any iteration j > 1,
∥Xj -X(T )∥F ≤µalg∥Xj-1 -X(T )∥F + ξalg∥˜E∥F ,
(8)
then
∥Xj -X(T )∥F ≤
 µalgj ∥X0 -X(T )∥F +
ξalg
1 -µalg ∥˜E∥F .
(9)
**Lemma 3. If A ∈M(m, n) has ARIP constants Lk, Uk and**
Z ∈χn,l(k), then
(1 -Lk)∥Z∥2
F ≤∥AZ∥2
F ≤(1 + Uk)∥Z∥2
F .
(10)
Proof: For each column of Z, Definition 1 states (1 -
Lk)∥Zi∥2
2 ≤∥AZi∥2
2 ≤(1 + Uk)∥Zi∥2
2. Therefore, summing
over all columns in Z provides the ARIP statement in terms
of the Frobenius norm.
**Lemma 4. Let A ∈M(m, n) have ARIP constants Lk and**
Uk, and let T j be the index set from the DetectSupport
step in iteration j of SNIHT or SNHTP (Algorithms 1 or 2).
Then, wj+1, the optimal steepest descent step size in iteration
j + 1 of SNIHT or SNHTP, satisfies
1
1 + Uk
≤wj+1 ≤
1
1 -Lk
.
(11)
Proof: Let Zj
=
 A∗(Y -AXj)

(T j) where Y
∈
M(m, l) is the input measurements and Xj is the approximation after iteration j for SNIHT or SNHTP. Then
wj+1 =
∥Zj∥2
F
∥AT jZj∥2
F
.
By Lemma 3,
(1 -Lk) ≤∥AT jZj∥2
F
∥Zj∥2
F
≤(1 + Uk),
and (11) follows.
**Lemma 5. Let A ∈M(m, n) with ARIP constants Lk, Lck,**
Uk, and Uck where k, ck ∈N. Let S be any column index
set with |S| = ck and let {wj}∞
j=1 be a sequence of positive
scalars. Then,
(i) if ωj = ω is constant for all j, then
∥I-ωA∗
SAS∥2 ≤max {|1 -ω(1 + Uck)| , |1 -ω(1 -Lck)|} ;
(ii) if
1
1+Uk ≤ωj ≤
1
1-Lk for all j, then
∥I -ωjA∗
SAS∥2 ≤Uck + Lck
1 -Lk
.
Proof: From Definition 1 and as described in [21], the
ARIP constants are equal to extreme eigenvalues on the set of
all Gram matrices comprised of ck columns of A:
1 -Lck =
min
Q:|Q|=ck λ
 A∗
QAQ

;
1 + Uck =
max
Q:|Q|=ck λ
 A∗
QAQ

.
Hence, for any set S with |S| = ck, 1 -Lck ≤λ(A∗
SAS) ≤
1+Uck. Therefore, the eigenvalues of the matrix I -ωjA∗
SAS
are bounded by
1 -ωj(1 + Uck) ≤λ
 I -ωjA∗
SAS

≤1 -ωj(1 -Lck).
In case (i),
∥I -ωA∗
SAS∥2 = max

λ
 I -ωjA∗
SAS


≤max {|1 -ω(1 + Uck)| , |1 -ω(1 -Lck)|} .
In case (ii), for each j Lemma 4 ensures
1 -
1
1 -Lk
(1 + Uck) ≤1 -ωj(1 + Uck),
1 -
1
1 + Uk
(1 -Lck) ≥1 -ωj(1 -Lck).
Hence,
-Uck -Lk
1 -Lk
≤λ
 I -ωjA∗
SAS

≤Uk + Lck
1 + Uk
.



<!-- page: 9 -->

Thus
∥I -ωA∗
SAS∥2 ≤max

λ
 I -ωjA∗
SAS


≤max


-Uck -Lk
1 -Lk

 ,

Uk + Lck
1 + Uk


= max
Uck + Lk
1 -Lk
, Uk + Lck
1 + Uk

.
Since Uk ≤Uck, Lk ≤Lck, and 1-Lk ≤1+Uk, (ii) follows
from the bound
max
Uck + Lk
1 -Lk
, Uk + Lck
1 + Uk

≤Uck + Lck
1 -Lk
.
### B. Algorithm Specific Theorems
The following theorem and its proof are representative of
the analysis for all five greedy algorithms. This proof includes
the use of ARIP constants and simultaneously treats both fixed
and normalized step-sizes. The proof is based on the IHT proof
of Foucart [20].
**Theorem 2 (SIHT and SNIHT). Let X ∈M(n, l) and let T**
be the row index set for the k rows of X with largest ℓ2 norm.
Let A ∈M(m, n) with ARIP constants Lk, L3k, U2k, and U3k,
and let ϕ(3k) be a function of ARIP constants such that for all
ωj in Algorithm 1, ∥I-ωjA∗
QAQ∥2 ≤ϕ(3k) < 1 for all index
sets Q with |Q| = 3k. Define Y = AX + E = AX(T ) + ˜E
for some error matrix E ∈M(m, l) and ˜E = AX(T c) + E.
Define the ARIP functions
µ1(k) = 2ϕ(3k)
(12)
ξ1(k) = 2(max
j
ωj)
p
1 + U2k.
(13)
If {Xj} is the sequence of approximations from SIHT or
SNIHT (Algorithm 1), then for all j
∥Xj+1-X(T )∥F ≤µ1(k)∥Xj -X(T )∥F +ξ1(k)∥˜E∥F . (14)
Proof: Let V j = Xj+wjA∗(Y -AXj) be the update step
from Algorithm 1. By substituting Y = AX(T ) + AX(T c) +
E = AX(T ) + ˜E, we have
V j = Xj + ωjA∗A(X(T ) -Xj) + ωjA∗˜E.
(15)
By the DetectSupport and Threshold steps in Algorithm 1, Lemma 1 implies
∥V j -Xj+1∥2
F ≤∥V j -X(T )∥2
F .
(16)
Writing V j = V j -X(T ) + X(T ), the left hand side of (16)
can be expanded via the Frobenius inner product to reveal
∥V j -Xj+1∥2
F = ∥V j -X(T )∥2
F + ∥X(T ) -Xj+1∥2
F
-2

REAL
 
V j -X(T ), X(T ) -Xj+1

F

.
(17)
Combining (16) and (17) and bounding the real part of the
inner product by its magnitude,
∥X(T ) -Xj+1∥2
F ≤2

V j -X(T ), X(T ) -Xj+1

 . (18)
From (15),
V j -X(T ) = (I -ωjA∗A)(Xj -X(T )) + ωjA∗˜E,
so applying the triangle inequality to (18), we have
∥Xj+1 -X(T )∥2
F
≤2

(I -ωjA∗A)(Xj -X(T )), (Xj+1 -X(T ))

+ 2ωj

D
˜E, A(Xj+1 -X(T ))
E

= 2

(I -ωjA∗
QAQ)(Xj -X(T )), (Xj+1 -X(T ))

+ 2ωj

D
˜E, A(Xj+1 -X(T ))
E

(19)
where Q = T ∪T j ∪T j+1.
Now, let ϕ(3k) be a function of ARIP constants such that for
any set Q with |Q| = 3k, we have ∥I -ωjA∗
QAQ∥2 ≤ϕ(3k).
Then
|⟨(I -ωjA∗
QAQ)(Xj -X(T )), (Xj+1 -X(T ))

≤ϕ(3k)∥Xj -X(T )∥F ∥Xj+1 -X(T )∥F .
(20)
By Definition 1 and the Cauchy-Schwartz inequality,

D
˜E, A(Xj+1 -X(T ))
E

 ≤
p
1 + U2k∥˜E∥F ∥Xj+1-X(T )∥F .
(21)
With (20) and (21), (19) simplifies to
∥Xj+1-X(T )∥F ≤2ϕ(3k)∥Xj-X(T )∥F +2ωjp
1 + U2k∥˜E∥F ,
(22)
establishing (14).
The proofs of the following theorems are presented in [26]
for completeness. The proofs closely follow the analysis for
the SMV variants presented by Foucart [20] while incorporating ARIP constants and simultaneously treating fixed and
normalised step-sizes.
**Theorem 3 (SHTP and SNHTP). Let X ∈M(n, l) and let**
T be the row index set for the k rows of X with largest ℓ2
norm. Let A ∈M(m, n) with ARIP constants Lck and Uck for
c = 1, 2, 3, and let ϕ(ck) be a function of ARIP constants such
that for all ωj in Algorithm 2, ∥I -ωjA∗
QAQ∥2 ≤ϕ(ck) < 1
for all index sets Q with |Q| = ck. Define Y = AX + E =
AX(T ) + ˜E for some error matrix E ∈M(m, l) and ˜E =
AX(T c) + E. Define the ARIP functions
µ2(k) =
s
2 [ϕ(3k)]2
1 -[ϕ(2k)]2
(23)
ξ2(k) =
s
2(1 + U2k)
1 -[ϕ(2k)]2 + (max
j
ωj)
√1 + Uk
1 -ϕ(2k).
(24)
If {Xj} is the sequence of approximations from SHTP or
SNHTP (Algorithm 2), then for all j
∥Xj+1-X(T )∥F ≤µ2(k)∥Xj -X(T )∥F +ξ2(k)∥˜E∥F . (25)
**Theorem 4 (SCoSaMP). Let X ∈M(n, l) and let T be the**
row index set for the k rows of X with largest ℓ2 norm. Let
A ∈M(m, n) with ARIP constants Lck and Uck for c =
2, 3, 4, and let ϕ(ck) be a function of ARIP constants such
that ∥I -A∗
QAQ∥2 ≤ϕ(ck) < 1 for all index sets Q with
|Q| = ck. Define Y = AX + E = AX(T ) + ˜E for some error



<!-- page: 10 -->

matrix E ∈M(m, l) and ˜E = AX(T c) + E. Define the ARIP
functions
µ3(k) =
s
(ϕ(2k) + ϕ(4k))2 (1 + 3[ϕ(4k)]2)
1 -[ϕ(4k)]2
(26)
ξ3(k) =
p
3(1 + U3k)
+
p
1 + 3[ϕ(4k)]2
 s
2(1 + U4k)
1 -[ϕ(4k)]2 +
s
1 + U3k
1 -ϕ(4k)
!
.
(27)
If {Xj} is the sequence of approximations from SCoSaMP
(Algorithm 3), then for all j
∥Xj+1-X(T )∥F ≤µ3(k)∥Xj -X(T )∥F +ξ3(k)∥˜E∥F . (28)
### C. Proof of Main Results
Proof of Theorem 1:
For the fixed step size variants
SIHT or SHTP, Lemma 5 ensures that the ARIP function
ϕ(ck) from Theorems 2 and 3 can be chosen to be the
function φω(ck) = max{|1 -ω(1 + Uck)|, |1 -ω(1 -Lck)|}.
Likewise, for the normalised variants SNIHT and SNHTP,
**Lemma 5 ensures that the optimal subspace restricted steepest descent steps permit the substitution of ARIP function**
ψ(ck) = Uck+Lck
1-Lk
for the ARIP function ϕ(ck) in Theorems 2
and 3. Finally, for SCoSaMP, it is clear that we can select
ϕ(4k) = max{U4k, L4k} = R4k.
All three choices of ARIP functions are nondecreasing. In
the following, each ARIP function µalg(k; A) is defined in
Table I. Therefore, it is clear that with ϕ(ck) = φω(ck),
µ1(k) ≤µsiht(k; A),
(29)
µ2(k) ≤µshtp(k; A).
(30)
For ϕ(ck) = ψ(ck),
µ1(k) ≤µsniht(k; A),
(31)
µ2(k) ≤µsnhtp(k; A).
(32)
Finally, with ϕ(4k) = R4k,
µ3(k) ≤µscosamp(k; A).
(33)
The sufficient ARIP conditions in Table I guarantee that
the associated ARIP functions µalg(k; A) < 1. Therefore,
combining Lemma 2 with Theorems 2-4 proves Theorem 1.
Proof of Corollary 1:
In the ideal setting where T =
supp(X) and E = 0, with X0 = 0 (5) follows directly from
**Theorem 1. The number of iterations follows from a minor**
generalization of analogous results in [2], [23] since it is clear
that
∥Xjalg
max -X∥F < min
i∈T ∥X(i)∥2
and therefore supp(Xjalg
max) ⊂supp(X).
REFERENCES
[1] B. K. Natarajan, "Sparse approximate solutions to linear systems," SIAM
### J. Computing, vol. 24, no. 2, pp. 227-234, 1995.
[2] S. Foucart, "Recovering jointly sparse vectors via hard thresholding
pursuit," in Proc. of SAMPTA, 2011, Online.
[3] J. A. Tropp, A. C. Gilbert, and M. J. Strauss, "Algorithms for simultaneous sparse approximation. Part I: Greedy pursuit," Signal Processing,
vol. 86, pp. 572-588, 2006.
[4] D. Leviatan and V. N. Temlyakov, "Simultaneous approximation by
greedy algorithms," Adv. Comput. Math., vol. 25, no. 1-3, pp. 73-90,
2006.
[5] A. Lutoborski and V. N. Temlyakov, "Vector greedy algorithms," J.
Complexity, vol. 19, no. 4, pp. 458-473, 2003.
[6] V. N. Temlyakov, "A remark on simultaneous greedy approximation,"
East J. Approx., vol. 10, no. 1-2, pp. 17-25, 2004.
[7] J. Chen and X. Huo, "Theoretical results on sparse representations of
multiple-measurement vectors," IEEE Trans. Sig. Proc., vol. 54, no. 12,
pp. 4634-4643, 2006.
[8] S. Cotter, B. Rao, K. Engan, and K. Kreutz-Delgado, "Sparse solutions
to linear inverse problems with multiple measurement vectors," IEEE
Trans. Sig. Proc., vol. 53, no. 7, pp. 2477-2488, 2005.
[9] M. E. Davies and Y. C. Eldar, "Rank awareness in joint sparse recovery,"
IEEE Trans. Inform. Theory, vol. 58, no. 2, pp. 1135-1146, 2012.
[10] Y. Eldar and M. Mishali, "Robust recovery of signals from a structured
union of subspaces," IEEE Trans. Inform. Theory, vol. 55, no. 11, pp.
5302-5316, 2009.
[11] Y. Eldar and H. Rauhut, "Average case analysis of multichannel sparse
recovery using convex relaxation," IEEE Trans. Inform. Theory, vol. 56,
no. 1, pp. 505-519, 2010.
[12] K. Lee, Y. Bresler, and M. Junge, "Subspace methods for joint sparse
recovery," IEEE Trans. Inform. Theory, vol. 58, no. 6, pp. 3613-3641,
2012.
[13] M.-J. Lai and Y. Liu, "The null space property for sparse recovery from
multiple measurement vectors," Appl. Comp. Harmon. Anal., vol. 30,
no. 3, pp. 402-406, 2011.
[14] E. van den Berg and M. Friedlander, "Theoretical and empirical results
for recovery from multiple measurements," IEEE Trans. Inform. Theory,
vol. 56, no. 5, pp. 2516-2527, 2010.
[15] J. A. Tropp, "Algorithms for simultaneous sparse approximation. Part
II: Convex relaxation," Signal Processing, vol. 86, pp. 589-602, 2006.
[16] S. Foucart, "Hard thresholding pursuit: an algorithm for compressive
sensing," SIAM J. Numerical Analysis, vol. 49, no. 6, pp. 2543-2563,
2011.
[17] T. Blumensath and M. E. Davies, "Iterative hard thresholding for
compressed sensing," Appl. Comput. Harmon. Anal., vol. 27, no. 3, pp.
265-274, 2009.
[18] --, "Normalised iterative hard thresholding; guaranteed stability and
performance," IEEE J. Selected Topics in Signal Processing, vol. 4, no. 2,
pp. 298-309, 2010.
[19] D. Needell and J. Tropp, "CoSaMP: Iterative signal recovery from
incomplete and inaccurate samples," Appl. Comput. Harmon. Anal.,
vol. 26, no. 3, pp. 301-321, 2009.
[20] S. Foucart, "Sparse recovery algorithms: Sufficient conditions in terms
of restricted isometry constants," in Approximation Theory XIII: San
Antonio 2010, ser. Springer Proceedings in Mathematics, M. Neamtu
and L. Schumaker, Eds.
Springer New York, 2012, vol. 13, pp. 65-77.
[21] J. D. Blanchard, C. Cartis, and J. Tanner, "Compressed Sensing: How
sharp is the restricted isometry property?" SIAM Review, vol. 53, no. 1,
pp. 105-125, 2011.
[22] A. Maleki and D. Donoho, "Optimally tuned iterative reconstruction
algorithms for compressed sensing," IEEE J. Selected Topics in Signal
Processing, vol. 4, no. 2, pp. 330 -341, april 2010.
[23] J. D. Blanchard, C. Cartis, J. Tanner, and A. Thompson, "Phase
transitions for greedy sparse approximation algorithms," Appl. Comput.
Harmon. Anal., vol. 30, no. 2, pp. 188-203, 2011.
[24] J. D. Blanchard and J. Tanner, "Performance comparisons of greedy
algorithms for compressed sensing," 2013, Submitted.
[25] J. Blanchard and M. Davies, "Recovery guarantees for rank aware
pursuits," IEEE Sig. Proc. Letters, vol. 19, no. 7, pp. 427-430, 2012.
[26] J. Blanchard, M. Cermak, D. Hanle, and Y. Jing, "Greedy algorithms for joint sparse recovery: supplementary material," 2013,
www.math.grinnell.edu/∼blanchaj/GAJSsupp.pdf.
[27] E. J. Candes and T. Tao, "Decoding by linear programming," IEEE
Trans. Inform. Theory, vol. 51, no. 12, pp. 4203-4215, 2005.
[28] D. L. Donoho and J. Tanner, "Precise undersampling theorems," Proceedings of the IEEE, vol. 98, no. 6, pp. 913-924, 2010.



<!-- page: 11 -->

[29] B. Bah and J. Tanner, "Improved bounds on restricted isometry constants
for gaussian matrices," SIAM Journal on Matrix Analysis, vol. 31, no. 5,
pp. 2882-2898, 2010.
[30] J. D. Blanchard and J. Tanner, "GPU accelerated greedy algorithms for
compressed sensing," Mathematical Programming Computation, vol. 5,
no. 3, pp. 267-304, 2013.
[31] --, "GAGA: GPU Accelerated Greedy Algorithms," 2013, version
1.0.0. [Online]. Available: www.gaga4cs.org
[32] D. L. Donoho and J. Tanner, "Counting faces of randomly projected
polytopes when the projection radically lowers dimension," J. AMS,
vol. 22, no. 1, pp. 1-53, 2009.
[33] --, "Neighborliness of randomly projected simplices in high dimensions," Proc. Natl. Acad. Sci. USA, vol. 102, no. 27, pp. 9452-9457
(electronic), 2005.
[34] R. O. Schmidt, "Multiple emitter location and signal parameter estimation," Proceedings of RADC Spectral Estimation Workshop, pp. 243-
258, 1979.
Jeffrey D. Blanchard recieved the B.A. (Hons.)
degree in mathematics from Benedictine College,
Atchison, KS, USA, in 1998. After serving as an
officer in the US Army, he recieved the A.M. and
Ph.D. degrees in mathematics from Washington University in St. Louis, St. Louis, MO, USA, in 2004
and 2007, respectively, where he held a Department
of Homeland Security Fellowship. From 2007 to
2009, he was a VIGRE Research Assistant Professor
in the Department of Mathematics at the University
of Utah, Salt Lake City, UT, USA. Since August
2009, he has been an Assistant Professor in the Department of Mathematics
and Statistics at Grinnell College, Grinnell, IA, USA. From January to
December 2010, he was a National Science Foundation International Research
Fellow at the School of Mathematics and the School of Electronics and
Engineering at the University of Edinburgh, Endiburgh, UK. He was a
2008-2009 Mathematical Association of America Project NExT Fellow and
a 2013-2014 Grinnell College Harris Faculty Fellow. His current research
interests include composite dilation wavelets, compressed sensing, matrix
completion, scientific computing with graphics processing units, and directing
undergraduate research.
Michael Cermak is a fourth-year student from Chotebor, Czech Republic,
double majoring in Mathematics & Statistics and Economics at Grinnell
College, Grinnell, IA, USA. In summer 2012, he conducted research in
compressed sensing with the group led by Professor Blanchard. During the
2012-2013 academic year, he completed a study abroad program at the London
School of Economics in London, UK and an internship the following summer
with JP Morgan in London. He intends to pursue graduate work and a career
in applied mathematics with a focus on industry.
David Hanle is a fourth-year student from Madison, WI, USA, double
majoring in Mathematics & Statistics and Computer Science at Grinnell
College, IA, USA. In summer 2012, he conducted research in compressed
sensing with the group led by Professor Blanchard. In summer 2013, he was an
intern with Administrative Information Management Services at the University
of Wisconsin - Madison. He hopes to pursue a career in software development.
Outside of the classroom, David enjoys playing sports and piano.
Yirong Jing is a fourth-year student from Taiyuan, Shanxi, China, double
majoring in Mathematics & Statistics and Economics at Grinnell College, IA,
USA. In summer 2012, she conducted research in compressed sensing with the
group led by Professor Blanchard. In fall 2012, she was a research assistant
in the Woodrow Wilson International Center for Scholars, Washington, DC.
In summer 2013, she participated in a machine learning research project led
by Professor Jerod Weinman at Grinnell College.



<!-- page: 12 -->

## Appendix B
GREEDY ALGORITHMS FOR JOINT SPARSE RECOVERY:
SUPPLEMENTARY MATERIAL
This document includes supplementary material for the
paper Greedy Algorithms for Joint Sparse Recovery and the
references to definitions, theorems, lemmas and equations
refer to that document. The numbering in this document
is a continuation of that in the main document. First, for
completeness the omitted proofs are included in Section B-A.
The analysis verifying the use of the asymptotic bounds on
the ARIP constants to determine the strong phase transition
curves in Section III-A is included here in Section B-B. Also,
various level curves for convergence and stability factors are
provided in Figure 5. The additional empirical weak phase
transitions for A drawn from the DCT matrix ensemble appear
in Section B-C.
### A. Omitted Proofs
In the following, if S, T are index sets, let T\S := {t ∈
T : t /∈S} and define the symmetric difference of the two
sets T∆S := (T ∪S)\(T ∩S). We first prove an additional
technical lemma utilized in the proofs of Theorems 3 and 4.
**Lemma 6. Let Z ∈M(n, l) and let S, T ⊂{1, 2, . . . , n} be**
row index sets. Then
∥ZT \S∥F + ∥ZS\T ∥F ≤
√
2∥ZT ∆S∥F .
(34)
Proof: For any real numbers a, b, 2ab ≤a2 + b2 so that
 ∥ZT \S∥F + ∥ZS\T ∥F
2 = ∥ZT \S∥2
F + ∥ZS\T ∥2
F
+ 2∥ZT \S∥F ∥ZS\T ∥F
≤2
 ∥ZT \S∥2
F + ∥ZS\T ∥2
F

= 2∥ZT ∆S∥2
F
and (34) is equivalent.
The following four proofs were omitted from the main
manuscript and are included here for completeness.
Proof of Lemma 1:
By the choice of T, ∥Z(T )∥2
F =
P
t∈T ∥Z(t)∥2
2 ≥P
s∈S ∥Z(s)∥2
2 = ∥Z(S)∥2
F . Thus,
∥Z -Z(T )∥2
F = ∥Z∥2
F -∥Z(T )∥2
F
≤∥Z∥2
F -∥Z(S)∥2
F = ∥Z -Z(S)∥2
F
and (7) is equivalent.
Proof of Lemma 2: This is a straightforward induction
argument. For X0 = 0, the base case is trivial. Assuming the
inductive hypotheses (9) for iteration j -1, then (8) implies
that at iteration j,
∥Xj -X(T )∥F ≤µalg
 µalgj-1 ∥X(T )∥F +
ξalg
1 -µalg ∥˜E∥F

+ ξalg∥˜E∥F ,
which is equivalent to (9) for iteration j.
Proof of Theorem 3: From the projection step in Algorithm 2, Y -AXj+1 is Frobenius-orthogonal to the subspace
{AZ
: supp(Z) ⊂T j+1}. Letting Y
= AX + E
=
AX(T ) +AX(T c) +E = AX(T ) + ˜E, we have Y -AXj+1 =
A(X(T ) -Xj+1) + ˜E. Therefore, for all vectors Z with
supp(Z) ⊂T j+1,
0 =

Y -AXj+1, AZ

=

A(X(T ) -Xj+1), AZ

+
D
˜E, AZ
E
=

Xj+1 -X(T ), -A∗AZ

+
D
˜E, AZ
E
.
(35)
Select Z = (Xj+1 -X(T ))(T j+1) so that
∥Z∥2
F = ∥(Xj+1 -X(T ))(T j+1)∥2
F
=

Xj+1 -X(T ), (Xj+1 -X(T ))(T j+1)

=

Xj+1 -X(T ), Z

.
Scaling (35) by ωj and adding 0 to ∥Z∥2
F yields
∥Z∥2
F =

Xj+1 -X(T ), (I -wjA∗A)Z

+
D
wj ˜E, AZ
E
.
(36)
Now, let ϕ(ck) be a function of ARIP constants such that
for any set Q with |Q| = ck, we have ∥I -ωjA∗
QAQ∥2 ≤
ϕ(ck) < 1. Then with Q = T ∪T j+1, the first term in the
right hand side of (36) is bounded above by

Xj+1 -X(T ), (I -wjA∗A)Z

=

Xj+1 -X(T ), (I -wjA∗
QAQ)Z

≤ϕ(2k)∥Xj+1 -X(T )∥F ∥Z∥F .
(37)
The second term of (36) is bounded above by
D
wj ˜E, AZ
E
≤wjp
1 + Uk∥˜E∥F ∥Z∥F .
(38)
Applying the bounds (37) and (38) to (36),
∥Z∥F ≤ϕ(2k)∥Xj+1 -X(T )∥F + wjp
1 + Uk∥˜E∥F . (39)
Let W = (Xj+1 -X(T ))((T j+1)c) so that Xj+1 -X(T ) =
Z + W. Then, by (39)
∥Xj+1 -X(T )∥2
F -∥W∥2
F = ∥Z∥2
F
≤

ϕ(2k)∥Xj+1 -X(T )∥F + wjp
1 + Uk∥˜E∥F
2
= [ϕ(2k)]2 ∥Xj+1 -X(T )∥2
F +

wjp
1 + Uk
2
∥˜E∥2
F
+ 2ϕ(2k)

wjp
1 + Uk

∥Xj+1 -X(T )∥F ∥˜E∥F .
(40)
Define the convex polynomial
p(t) =

1 -[ϕ(2k)]2
t2 -

2ϕ(2k)wjp
1 + Uk∥˜E∥F

t
-

∥W∥2
F +

wjp
1 + Uk
2
∥˜E∥2
F

.
The larger root t⋆of p(t) is therefore
t⋆=
ϕ(2k)
1 -[ϕ(2k)]2 wjp
1 + Uk∥˜E∥F
+
r
1 -[ϕ(2k)]2
∥W∥2
F +
 wj√1 + Uk
2 ∥˜E∥2
F
1 -[ϕ(2k)]2
.



<!-- page: 13 -->

By the sub-additivity of the square root,
t⋆≤
1 + ϕ(2k)
1 -[ϕ(2k)]2 wjp
1 + Uk∥˜E∥F +
1
q
1 -[ϕ(2k)]2 ∥W∥F .
(41)
By (40), p(∥Xj+1 -X(T )∥F ) ≤0 and therefore ∥Xj+1 -
X(T )∥F ≤t⋆. (41) implies
∥Xj+1 -X(T )∥F ≤
∥W∥F
q
1 -[ϕ(2k)]2 + wj√1 + Uk
1 -ϕ(2k) ∥˜E∥F .
(42)
To complete the proof, we find an upper bound for ∥W∥F .
Let V j = Xj + ωjA∗(Y -AXj) be the update step for
Algorithm 2. The DetectSupport step selects T j+1 so that
∥V j
(T )∥F ≤∥V j
(T j+1)∥F and therefore
∥V j
(T \T j+1)∥F ≤∥V j
(T j+1\T )∥F .
(43)
Substituting Y = AX(T ) + ˜E,
V j = Xj + ωjA∗A(X(T ) -Xj) + ωjA∗˜E
= X(T ) + (I -ωjA∗A)(Xj -X(T )) + ωjA∗˜E.
(44)
With supp(Xj+1) = T j+1, (X(T ))(T \T j+1)
= (X(T ) -
Xj+1)(T \T j+1) and since W = (Xj+1 -X(T ))((T j+1)c) =
(Xj+1 -X(T ))(T \T j+1), V j
(T \T j+1) can be written
V j
(T \T j+1) = -W + ωj(A∗˜E)(T \T j+1)
+ (I -ωjA∗A)(Xj -X(T ))(T \T j+1).
(45)
Therefore, the left hand side of (43) can be bounded below
by applying the reverse triangle inequality to (45);
∥V j
(T \T j+1)∥F ≥∥W∥F -ωj

(A∗˜E)(T \T j+1)

F
-

(I -ωjA∗A)(Xj -X(T ))(T \T j+1)

F . (46)
Since (X(T ))(T j+1\T ) = 0, (44) permits the straightforward
upper bound on the right hand side of (43),
∥V j
(T j+1\T )∥F ≤

(I -ωjA∗A)(Xj -X(T ))(T j+1\T )

F
+ ωj

(A∗˜E)(T j+1\T )

F .
(47)
Applying (46), (47) and Lemma 6 to (43) establishes
∥W∥F ≤
√
2

(I -ωjA∗A)(Xj -X(T ))(T ∆T j+1)

F
+
√
2ωj

(A∗˜E)(T ∆T j+1)

F .
(48)
With Q = T ∪T j ∪T j+1, the first norm on the right hand
side of (48) satisfies

(I -ωjA∗A) (Xj -X(T ))(T ∆T j+1)

F
≤

(I -ωjA∗
QAQ)(Xj -X(T ))

F
≤ϕ(3k)

(Xj -X(T ))

F ,
(49)
while the second norm of (48) satisfies

(A∗˜E)(T ∆T j+1)

F ≤
p
1 + U2k∥˜E∥F .
(50)
Hence, (49) and (50) yield
∥W∥F ≤
√
2ϕ(3k)

(Xj -X(T ))

F +
p
2(1 + U2k)∥˜E∥F .
(51)
Therefore, combining (42) and (51) establishes (25).
Proof of Theorem 4: From the projection step in Algorithm 3, Y -AU j is Frobenius-orthogonal to the subspace
{AZ : supp(Z) ⊂Qj = Sj ∪T j}. By an argument almost
identical to that at the beginning of the proof of Theorem 3,
we establish the upper bound
∥(U j-X(T ))(Qj)∥F ≤ϕ(4k)∥U j-X(T )∥F +
p
1 + U3k∥˜E∥F
(52)
where ϕ(4k) is any function of ARIP constants such that ∥I -
A∗
QAQ∥2 ≤ϕ(4k) < 1 for any index set Q with |Q| = 4k.
In this case Q = Qj ∪T ensures |Q| ≤4k.
Let W = (U j -X(T ))((Qj)c) so that U j -X(T ) = W +
(U j -X(T ))(Qj). Then (52) implies
∥U j -X(T )∥2
F ≤∥W∥2
F
+

ϕ(4k)∥U j -X(T )∥F +
p
1 + U3k∥˜E∥F
2
.
(53)
Define the convex polynomial
p(t) =

1 -[ϕ(4k)]2
t2 -

2ϕ(4k)
p
1 + U3k∥˜E∥F

t
-

∥W∥2
F + (1 + U3k) ∥˜E∥2
F

.
Again, as in the proof of Theorem 3, since (53) ensures
p(∥U j -X(T )∥F ) ≤0, bounding the larger root of p(t) via
the sub-additivity of the square root produces
∥U j -X(T )∥F ≤
∥W∥F
q
1 -[ϕ(4k)]2 +
√1 + U3k
1 -ϕ(4k)∥˜E∥F . (54)
Since Xj+1 -X(T ) = (U j -X(T )) -(U j -Xj+1),
expanding the norm and bounding the real part of the inner
product with its magnitude as in the proof of Theorem 2, we
have
∥Xj+1 -X(T )∥2
F ≤

U j -X(T )

2
F +

U j -Xj+1

2
F
+ 2

U j -X(T ), U j -Xj+1

 .
(55)
Applying the triangle and Cauchy-Schwartz inequalities
followed by an ARIP bound, we have

U j -X(T ),
U j -Xj+1

≤ϕ(4k)

U j -X(T )

F

U j -Xj+1

F
+
p
1 + U3k∥˜E∥F

U j -Xj+1

F .
(56)
Note
that
supp(U j -Xj+1)
=
Qj
and
by
the
DetectSupport and Threshold steps in Algorithm 3,
**Lemma 1 ensures**
∥U j -Xj+1∥F ≤∥(U j -X(T ))(Qj)∥F .
(57)
Therefore, applying (52), (56), and (57) to (55), and rearranging yields
∥Xj+1-X(T )∥2
F ≤(1 + 3[ϕ(4k)]2)∥U j -X(T )∥2
F
+ 6ϕ(4k)
p
1 + U3k∥U j -X(T )∥F ∥˜E∥F
+ 3(1 + U3k)∥˜E∥2
F .
(58)



<!-- page: 14 -->

Since 36[ϕ(4k)]2
≤
12 + 36[ϕ(4k)]2, then 6ϕ(4k)
≤
2
p
3(1 + 3[ϕ(4k)]2). Using this observation to bound (58)
and simplifying produces the bound
∥Xj+1 -X(T )∥2
F ≤
p
1 + 3[ϕ(4k)]2∥U j -X(T )∥F
+
p
3(1 + U3k)∥˜E∥F .
(59)
To complete the proof via (54), we establish an upper
bound on ∥W∥F . Notice that supp(Xj), supp(U j) ⊂Qj, and
therefore W = (U j -X(T ))((Qj)c) = (Xj -X(T ))((Qj)c).
Also, since Qj = Sj ∪T j, then (Qj)c ⊂(Sj)c and thus
∥W∥F ≤∥(Xj -X(T ))((Sj)c)∥F
= ∥(Xj -X(T ))((T ∪T j)\Sj)∥F .
(60)
By the definition of Sj from Algorithm 3, Lemma 1 implies

 A∗(Y -AXj)

((T ∪T j)\Sj)

F
≤

 A∗(Y -AXj)

(Sj\(T ∪T j))

F .
(61)
Writing Y
= AX(T ) + ˜E and observing that (Xj -
X(T ))(Sj\(T ∪T j)) = 0, the argument of the norm on the right
side of (61) can be written
 A∗(Y -AXj)

(Sj\(T ∪T j))
=
 A∗A(X(T ) -Xj)

(Sj\(T ∪T j)) +

A∗˜E

(Sj\(T ∪T j))
=
 (I -A∗A)(Xj -X(T ))

(Sj\(T ∪T j)) +

A∗˜E

(Sj\(T ∪T j)) .
(62)
Letting Q = T ∪Qj = T ∪T j ∪Sj,

 A∗(Y -AXj)

(Sj\(T ∪T j))

F
≤

 (I -A∗
QAQ)(Xj -X(T ))


F +


A∗˜E

(Sj\(T ∪T j))

F
≤ϕ(4k)

Xj -X(T )

F +


A∗˜E

(Sj\(T ∪T j))

F
.
(63)
Similarly,
 A∗(Y -AXj)

((T ∪T j)\Sj)
=

A∗A(X(T ) -Xj) + A∗˜E

((T ∪T j)\Sj)
= (Xj -X(T ))((T ∪T j)\Sj)
-
 (I -A∗A)(Xj -X(T ))

((T ∪T j)\Sj)
+

A∗˜E

(Sj\(T ∪T j))
(64)
Therefore, (60) and (64) provide a lower bound for the left
hand side of (61).

 A∗(Y -AXj)

((T ∪T j)\Sj)

F
≥∥W∥F -

(I -A∗
(T ∪T j)A(T ∪T j))(Xj -X(T ))

F
-


A∗˜E

(Sj\(T ∪T j))

F
≥∥W∥F -ϕ(2k)

Xj -X(T )

F -


A∗˜E

(Sj\(T ∪T j))

F
.
(65)
Applying (63) and (65) to (61), solving for ∥W∥F , and
applying Lemma 6 and the upper ARIP bound, we have
∥W∥F ≤(ϕ(2k)+ϕ(4k))

Xj -X(T )

F +
p
2(1 + U4k)∥˜E∥F .
(66)
Combining (54), (59), and (66) establishes (28).
### B. Strong Phase Transitions
Under the proportional growth asymptotic (m/n, k/m) →
(δ, ρ), computable bounds, L(δ, ρ), U(δ, ρ), on the ARIP constants, Lk, Uk, were established for matrices drawn from the
Gaussian ensemble [21]. The exact formulation of the bounds
is available in [21].
**Definition 2 (Proportional-Growth Asymptotic). A sequence**
of problem sizes (k, m, n) is said to grow proportionally if,
for (δ, ρ) ∈[0, 1]2, m
n →δ and
k
m →ρ as m →∞.
The following is an adaptation of [21, Thm. 1].
**Theorem 5 (Blanchard, Cartis, Tanner [21]). Fix ϵ > 0. Under**
the proportional-growth asymptotic, Definition 2, sample each
matrix A ∈M(m, n) from the Gaussian ensemble. Let L(δ, ρ)
and U(δ, ρ) be defined as in [21, Thm. 1]. Define R(δ, ρ) =
max{L(δ, ρ), U(δ, ρ)}. Then for any ϵ > 0, as m →∞,
Prob [Lk < L(δ, ρ) + ϵ] →1,
(67)
Prob [Uk < U(δ, ρ) + ϵ] →1,
(68)
and
Prob [Rk < R(δ, ρ) + ϵ] →1.
(69)
To employ the bounds on the ARIP constants in order to
define the strong phase transition curves ρalg
S (δ), the stability
factor µalg(k; A) and stability factor ξalg
S (δ) must satisfy the
sufficient conditions of the following lemma:
**Lemma 7 (Lemma 12, [23]). For some τ < 1, define the set**
Ω:= (0, τ)p × (o, ∞)q and let F : Ω→R be continuously
differentiable on Ω. Let A be a Gaussian matrix of size
m × n with ARIP constants Lk, . . . , Lpk, Uk, . . . , Uqk. Let
L(δ, ρ), U(δ, ρ) be the ARIP bounds defined in Theorem 5.
Define 1 to be the vector of all ones, and
z(k) := [Lk, . . . , Lpk, Uk, . . . , Uqk] ,
(70)
z(δ, ρ) := [L(δ, ρ), . . . , L(δ, pρ), U(δ, ρ), . . . , U(δ, qρ)] .
(71)
(i) Suppose, for all t ∈Ω, (∇F[t])i ≥0 for all i =
1, . . . , p + q and for any v ∈Ωwe have ∇F[t] · v > 0.
Then for any cϵ > 0, as (k, m, n) →∞with
m
n →
δ, k
n →ρ, there is overwhelming probability on the draw
of the matrix A that
Prob (F[z(k)] < F[z(δ, ρ) + 1cϵ]) →1
as m →∞.
(72)
(ii) Suppose, for all t ∈Ω, (∇F[t])i ≥0 for all i =
1, . . . , p + q and there exists j ∈{1, . . . , p} such that
(∇F[t])j > 0. Then there exists c ∈(0, 1) depending
only on F, δ,and ρ such that for any ϵ ∈(0, 1)
F[z(δ, ρ) + 1cϵ] < F[z(δ, (1 + ϵ)ρ)],
(73)



<!-- page: 15 -->

and so there is overwhelming probability on the draw of
A that
Prob (F[z(k)] < F[z(δ, (1 + ϵ)ρ)]) →1
as m →∞.
(74)
Also, F(z(δ, ρ)) is strictly increasing in ρ.
**Definition 3. For (δ, ρ) ∈(0, 1)2, define the asymptotic**
bounds on the convergence factors as follows:
µsiht(δ, ρ) := 2R(δ, 3ρ);
(75)
µsniht(δ, ρ) := 2U(δ, 3ρ) + L(δ, 3ρ)
1 -L(δ, ρ)
;
(76)
µshtp(δ, ρ) :=
s
2[R(δ, 3ρ)]2
1 -[R(δ, 2ρ)]2 ;
(77)
µsnhtp(δ, ρ) :=
v
u
u
u
u
t
2

U(δ,3ρ)+L(δ,3ρ)
1-L(δ,ρ)
2
1 -

U(δ,2ρ)+L(δ,2ρ)
1-L(δ,ρ)
2 ;
(78)
µscosamp(δ, ρ) :=
s
4[R(δ, 4ρ)]2(1 + 3[R(δ, 4ρ)]2)
1 -[R(δ, 4ρ)]2
.
(79)
For SIHT with a fixed step size of ω⋆= 2/(2 + U(δ, 3ρ) -
L(δ, 3ρ)), the validity of employing the asymptotic ARIP
bounds was established in [23, A.4.]. For SIHT and SHTP with
a fixed step size of ω⋆= 1, we see that Lemma 5 establishes
that φ1(ck) = max{Uck, Lck} = Rck is a valid selection, and
thus from Table I we have
µshtp(k; A) =
s
2[R3k]2
1 -[R2k]2 .
This allows us to state the following theorem.
**Theorem 6. Suppose A ∈M(m, n) is drawn from the Gaussian ensemble and that A has RIP constants R2k, R3k < 1.**
Consider SHTP with fixed step size ω⋆= 1. Then for any
ϵ > 0, there is overwhelming probability on the draw of A
that
µshtp(k; A) < µshtp(δ, (1 + ϵ)ρ).
(80)
Proof: Fix τ < 1 and let Ω= (0, τ)2. For t ∈Ωdefine
F[t] =
2t2
2
1 -t2
1
.
Clearly, F satisfies the conditions of Lemma 7 since
∇F[t] =

4t2
2t1
(1 -t2
1)2 ,
4t2
1 -t2
1

> 0.
Now let
z(k) = [R2k, R3k]
z(δ, ρ) = [R(δ, 2ρ), R(δ, 3ρ)].
Then with overwhelming probability on the draw of A,
F[z(k)] < F[z(δ, (1 + ϵ)ρ)].
Finally, we see that with overwhelming probability on the draw
of A,
µshtp(k; A) =
p
F[z(k)]
<
p
F[z(δ, (1 + ϵ)ρ)]
= µshtp(δ, (1 + ϵ)ρ).
The arguments establishing the validity of the bounds
µsiht(δ, ρ) and µscosamp(δ, ρ) are similar to the argument
for Theorem 6 and are therefore omitted. We now establish
the validity of the asymptotic bounds for the normalized
algorithms, SNIHT and SNHTP. To do so, recall the ARIP
function ψ(ck) from Table I:
ψ(ck) := Uck + Lck
1 -Lk
.
(81)
Therefore we introduce the following functions defined on the
set Ω= (0, τ)3 × (0, ∞)2 for any τ < 1:
F ψ
2 [t] = t4 + t2
1 -t1
;
(82)
F ψ
3 [t] = t5 + t3
1 -t1
.
(83)
These functions have nonnegative gradients since
∇F ψ
2 [t] =
 t4 + t2
(1 -t1)2 , t4 + 1
1 -t1
, 0, 1 + t2
1 -t1
, 0

;
(84)
∇F ψ
3 [t] =
 t5 + t3
(1 -t1)2 , 0, t5 + 1
1 -t1
, 0, 1 + t3
1 -t1

.
(85)
For the proofs of both of the following theorems, define
z(k) := [Lk, L2k, L3k, U2k, U3k],
(86)
z(δ, ρ) := [L(δ, ρ), L(δ, 2ρ), L(δ, 3ρ), U(δ, 2ρ), U(δ, 3ρ)].
(87)
**Theorem 7. Suppose A ∈M(m, n) is drawn from the Gaussian ensemble and that A has ARIP constants Lk, L3k, U3k.**
Then for any ϵ > 0, there is overwhelming probability on the
draw of A that
µsniht(k; A) < µsniht(δ, (1 + ϵ)ρ).
(88)
Proof: Fix τ < 1 and let Ω= (0, τ)3 × (0, ∞)2. From
(81), (83), and (86), we see that
ψ(3k) = F ψ
3 [z(k)],
and from (76), (83), and (87), we have
F ψ
3 [z(δ, ρ)] = 1
2µsniht(δ, ρ).
(85) establishes that F ψ
3
satisfies the conditions to invoke
**Lemma 7. Thus, with overwhelming probability on the draw**
of A,
µsniht(k; A) = 2ψ(3k) = 2F ψ
3 [z(k)]
< 2F ψ
3 [z(δ, (1 + ϵ)ρ)] = µsniht(δ, (1 + ϵ)ρ).
**Theorem 8. Suppose A**
∈
M(m, n) is drawn from
the Gaussian ensemble and that A has ARIP constants



<!-- page: 16 -->

Lk, L2k, L3k, U2k, U3k with U2k + L2k + Lk < 1. Then for
any ϵ > 0, there is overwhelming probability on the draw of
A that
µsnhtp(k; A) < µsnhtp(δ, (1 + ϵ)ρ).
(89)
Proof: Fix τ < 1 and let Ω= (0, τ)3 × (0, ∞)2. Restrict
the domain to the set ˜Ω= {t ∈Ω: F ψ
2 [t] < 1}. Now define
F H[t] =
2(F ψ
3 [t])2
1 -(F ψ
2 [t])2 .
For i = 2, 4,
∂
∂ti
F H[t] =
4F ψ
2 [t](F ψ
3 [t])2 
∂
∂ti F ψ
2 [t]


1 -(F ψ
2 [t])2
2
> 0.
For i = 3, 5,
∂
∂ti
F H[t] =
4F ψ
3 [t]

∂
∂ti F ψ
3 [t]

1 -(F ψ
2 [t])2
> 0.
Finally,
∂
∂t1
F H[t] =
4F ψ
3 [t]

∂
∂t1 F ψ
3 [t]

+ 4F ψ
3 [t]F ψ
2 [t]Ψ[t]
1 -(F ψ
2 [t])2
,
where
Ψ[t] = F ψ
3 [t]
 ∂
∂t1
F ψ
2 [t]

-F ψ
2 [t]
 ∂
∂t1
F ψ
3 [t]

= t5 + t3
1 -t1
 t4 + t2
(1 -t1)2

-t4 + t2
1 -t1
 t5 + t3
(1 -t1)2

= 0.
Hence ∇F H[t] > 0 and thus F H[t] satisfies the conditions to
invoke Lemma 7. Thus, with overwhelming probability on the
draw of A,
µsnhtp(k; A) =
q
F H[z(k)]
<
q
F H[z(δ, (1 + ϵ)ρ)] = µsnhtp(δ, (1 + ϵ)ρ).
The preceding discussion establishes the validity of employing the bounds in Definition 3. Therefore for each algorithm,
we establish a probabilistic lower bound on the region of
the phase space in which a Gaussian matrix will satisfy the
sufficient condition µalg < 1. Following the work in [23],
defining ρalg
S (δ) as the solution to the equation µalg(δ, ρ) = 1,
if ρ < (1 -ϵ)ρalg
S (δ) for any ϵ > 0, µalg(δ, ρ) < 1. Since
µalg(k; A) < µalg(δ, ρ) < 1 with overwhelming probability
on the draw of A from the Gaussian ensemble, then with the
same probability the sufficient ARIP condition is satisfied. The
curves ρalg
S (δ) are displayed in Figure 1. Here we include
level sets for both the convergence factors µalg(δ, ρ) and the
stability factor
ξalg
1-µalg in Figure 5. The computations required
to demonstrate the validity of employing the bounds on the
stability functions ξalg have been omitted.
0.4
0.5
0.6
0.7
0.8
0.9
1
ρ=k/m
δ=m/n
Level Curves SNIHT Convergence Factor: µsniht
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
0.5
1
1.5
2
2.5
3
3.5
x 10
-4
5
10
15
20
30
50
100
µsniht=1 →
ρ=k/m
δ=m/n
Level Curves SNIHT Stability Factor: ξsniht/(1-µsniht)
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
0.5
1
1.5
2
2.5
3
3.5
x 10
-4
(a)
(b)
0.4
0.5
0.6
0.7
0.8
0.9
1
ρ=k/m
δ=m/n
Level Curves SNHTP Convergence Factor: µsnhtp
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
1
2
3
4
5
x 10
-4
5
10
15
20
30
50
100
µsnhtp=1 →
ρ=k/m
δ=m/n
Level Curves SNHTP Stability Factor: ξsnhtp/(1-µsnhtp)
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
1
2
3
4
5
x 10
-4
(c)
(d)
0.4
0.5
0.6
0.7
0.8
0.9
1
ρ=k/m
δ=m/n
Level Sets SCoSaMP Convergence Factor: µscosamp
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
1
2
3
4
5
6
7
x 10
-4
8
10
15
20
30
50
100
µscosamp=1 →
ρ=k/m
δ=m/n
Level Curves SCoSaMP Stability Factor: ξscosamp/(1-µscosamp)
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
1
2
3
4
5
6
7
x 10
-4
(e)
(f)
Fig. 5.
Level sets for the convergence factors µalg(δ, ρ) and the stability
factors
ξalg
1-µalg (δ, ρ), in the left and right panels respectively: SNIHT (a),(b);
SNHTP (c),(d); SCoSaMP (e),(f).
### C. Weak Phase Transitions
1) Optimal Step Size Selection: The increasing performance improvement of the normalized versions of Algorithms 1 and 2 as the number of jointly sparse vectors increases
was discussed for Gaussian matrices A in Section III-B1. The
improvement is more pronounced when A is constructed by
randomly selecting m rows of an n × n discrete cosine transform matrix (DCT). In this case, we say A is drawn from the
DCT ensemble. Figure 6 includes the performance comparison
of the fixed step size variants of the algorithms versus the
optimal step size (normalized) variants. For comparison, both
the DCT ensemble and the Gaussian ensemble are included.
For SIHT, the step size is fixed at ω = .65 while the step size
is fixed at ω = 1 for SHTP. In the SMV setting SHTP (ω = 1)



<!-- page: 17 -->

0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← SNIHT l = 1
← SIHT l = 1
← SNIHT l = 10
← SIHT l = 10
Recovery Phase Transitions: SNIHT vs. SIHT, DCT Matrix Ensemble
δ=m/n
ρ=k/m
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← SNIHT l = 1
← SIHT l = 1
← SNIHT l = 10
← SIHT l = 10
Recovery Phase Transitions: SNIHT vs. SIHT, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(a)
(b)
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← SNHTP l = 1
← SHTP l = 1
← SNHTP l = 10
← SHTP l = 10
Recovery Phase Transitions: SNHTP vs. SHTP, DCT Matrix Ensemble
δ=m/n
ρ=k/m
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← SNHTP l = 1
← SHTP l = 1
← SNHTP l = 10
← SHTP l = 10
Recovery Phase Transitions: SNHTP vs. SHTP, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(c)
(d)
Fig. 6.
Empirical weak recovery phase transitions: fixed versus optimal Step
Size. SIHT versus SNIHT (a),(b) and SHTP versus SNHTP (c),(d). Matrix
ensembles DCT (left panels) and Gaussian (right panels).
and SNHTP have similar performance under the Gaussian
ensemble; when A is drawn from the DCT ensemble there is a
more pronounced improvement of SNHTP over SHTP . For A
drawn from the DCT ensemble, both SNIHT and SNHTP show
an increased performance improvement over SIHT and SHTP,
respectively, than for A drawn from the Gaussian ensemble.
2) Exact Recovery: For the exact recovery scenario, all
three algorithms, SNIHT, SHTP, SCoSaMP show improved
performance when A is drawn from the DCT ensemble
rather than the Gaussian ensemble. The lone exception to this
observation is SCoSaMP in the region m/n →0. Figure 7
shows the empirical weak phase transitions for both the DCT
and Gaussian ensembles under the same experimental set-up
as described in Section III-B. For all three algorithms, the
ratio of the area below the recovery phase transition curves
for l = 2, 5, 10 compared to the area below the curve for
l = 1 are given in Table II.
For A from the DCT ensemble, the discrepancy between the
three algorithms' performance is reduced as shown in Figure 8.
All three algorithms behave similarly through most of the
phase space although SCoSaMP demonstrates a difficulty for
m/n →0, a finding consistent with that in [24].
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SNIHT, DCT Matrix Ensemble
δ=m/n
ρ=k/m
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SNIHT, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(a)
(b)
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SNHTP, DCT Matrix Ensemble
δ=m/n
ρ=k/m
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SNHTP, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(c)
(d)
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SCoSaMP, DCT Matrix Ensemble
δ=m/n
ρ=k/m
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
← l = 1
← l = 2
← l = 5
l = 10 →
Recovery Phase Transitions: SCoSaMP, Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(e)
(f)
Fig. 7.
Empirical weak recovery phase transitions for various joint sparsity
levels with matrix ensembles DCT (left panels) and Gaussian (right panels).
SNIHT (a),(b); SNHTP (c),(d); SCSMPSP (e),(f).
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
SCoSaMP l = 2 →
SCoSaMP l = 10 →
← SNHTP l = 2
← SNHTP l = 10
← SNIHT l = 2
← SNIHT l = 10
Recovery Phase Transitions: DCT Matrix Ensemble
δ=m/n
ρ=k/m
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
SCoSaMP l = 2 →
SCoSaMP l = 10 →
← SNHTP l = 2
← SNHTP l = 10
← SNIHT l = 2
← SNIHT l = 10
Recovery Phase Transitions: Gaussian Matrix Ensemble
δ=m/n
ρ=k/m
(a)
(b)
Fig. 8.
Weak Recovery Phase Transitions with joint sparsity levels l = 2, 10
with matrix ensembles DCT (left panels) and Gaussian (right panels).
