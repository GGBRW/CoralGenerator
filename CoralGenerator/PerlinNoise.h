#ifndef PERLIN_NOISE_H
#define PERLIN_NOISE_H

#include <vector>

class PerlinNoise {
public:
    explicit PerlinNoise(unsigned int seed = 1999);

    double noise(double x, double y) const;

private:
    std::vector<int> p;

    static double fade(double t);
    static double lerp(double t, double a, double b);
    static double grad(int hash, double x, double y);
};

#endif
