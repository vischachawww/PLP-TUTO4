#include <iostream>
#include <algorithm>
using namespace std;

// 1. IN mode — Pass-by-value (NATIVE in C++)
// `mark` is a copy; modifying it does NOT affect the caller's variable.
int previewAdjustedMark(int mark, int bonus) {
    mark = min(mark + bonus, 100);
    return mark;
}

// 2. OUT mode — Pass-by-result (SIMULATED via reference, written only at exit)
void computeTotalAndAvg(int m1, int m2, int m3, int &outTotal, double &outAvg) {
    int localTotal = m1 + m2 + m3;
    double localAvg = localTotal / 3.0;
    outTotal = localTotal;   // copy-out at end
    outAvg = localAvg;       // copy-out at end
}

// 3. INOUT mode — Pass-by-value-result (SIMULATED via copy-in / copy-out)
void adjustMarkValueResult(int &mark, int bonus) {
    int localMark = mark;    // copy-in at start
    localMark = max(0, min(localMark + bonus, 100));
    mark = localMark;        // copy-out at end
}

// 4. INOUT mode — Pass-by-reference (NATIVE in C++ using `&`)
// `mark` is an alias for the caller's memory address; changes happen immediately.
void applyBonusByRef(int &mark, int bonus) {
    mark = max(0, min(mark + bonus, 100));
}

int main() {
    int aliMark = 70;

    // 1. Pass-by-value (NATIVE)
    int preview = previewAdjustedMark(aliMark, 10);
    cout << "[IN / Pass-by-value] preview=" << preview
         << ", caller aliMark=" << aliMark << " (unchanged)\n";

    // 2. Pass-by-result (SIMULATED)
    int total = 0;
    double avg = 0.0;
    computeTotalAndAvg(70, 85, 60, total, avg);
    cout << "[OUT / Pass-by-result] total=" << total << ", avg=" << avg << "\n";

    // 3. Pass-by-value-result (SIMULATED)
    int rajMark = 60;
    adjustMarkValueResult(rajMark, 8);
    cout << "[INOUT / Pass-by-value-result] rajMark=" << rajMark << "\n";

    // 4. Pass-by-reference (NATIVE)
    applyBonusByRef(aliMark, 5);
    cout << "[INOUT / Pass-by-reference] aliMark=" << aliMark << " (modified)\n";

    return 0;
}