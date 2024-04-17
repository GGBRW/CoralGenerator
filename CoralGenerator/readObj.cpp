#include <iostream>
#include <CGAL/Simple_cartesian.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/IO/OBJ.h>
#include <CGAL/Aff_transformation_3.h>
#include <fstream>

typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_3 Point_3;
typedef Kernel::Vector_3 Vector_3;
typedef CGAL::Surface_mesh<Point_3> Mesh;
typedef CGAL::Aff_transformation_3<Kernel> Transformation;

const unsigned int numberOfCorals = 16;

std::vector<Mesh> coralMeshes;

class Coral {
public:
    Point_3 position;
    double rotation; // Rotation around Z axis
    int type; // Coral type (in this case [0,1,2] for the three coral types) 

    Coral(const Point_3& pos, double rot, int t) : position(pos), rotation(rot), type(t) {}
};

bool readOBJ(const std::string& filename, Mesh& mesh) {
    std::ifstream input(filename);
    if (!input || !CGAL::IO::read_OBJ(input, mesh)) {
        std::cerr << "Error reading OBJ file: " << filename << std::endl;
        return false;
    } return true;
}

bool writeOBJ(const std::string& filename, const Mesh& mesh) {
    std::ofstream output(filename);
    if (!output || !CGAL::IO::write_OBJ(output, mesh)) {
        std::cerr << "Error writing OBJ file: " << filename << std::endl;
        return false;
    } return true;
}

Mesh combineMeshes(const std::vector<Coral>& corals) {
    Mesh combinedMesh;

    for (const auto& coral : corals) {
        // Copy mesh 
        Mesh transformedMesh = coralMeshes[coral.type]; 

        // Rotation matrix for rotation around the Y-axis
        double cos_theta = cos(coral.rotation);
        double sin_theta = sin(coral.rotation);
        Transformation rotate(CGAL::IDENTITY);
        rotate = Transformation(cos_theta, 0, sin_theta, 0, 1, 0, -sin_theta, 0, cos_theta);


        // Apply rotation
        for(auto v : transformedMesh.vertices()) {
            transformedMesh.point(v) = rotate(transformedMesh.point(v));
        }

        // Apply translation
        Transformation translate(CGAL::TRANSLATION, Vector_3(coral.position.x(), coral.position.y(), coral.position.z()));
        for(auto v : transformedMesh.vertices()) {
            transformedMesh.point(v) = translate(transformedMesh.point(v));
        }

        // Add transformed vertices and faces to the combined mesh
        std::map<Mesh::Vertex_index, Mesh::Vertex_index> vmap;
        for(auto v : transformedMesh.vertices()) {
            vmap[v] = combinedMesh.add_vertex(transformedMesh.point(v));
        }
        for(auto f : transformedMesh.faces()) {
            std::vector<Mesh::Vertex_index> vertices;
            for(auto v : vertices_around_face(transformedMesh.halfedge(f), transformedMesh)) {
                vertices.push_back(vmap[v]);
            }
            combinedMesh.add_face(vertices);
        }
    }

    return combinedMesh;
}


int main() {
    for(auto path : std::vector<std::string> { "../corals/cervicornis.obj", "../corals/secale.obj" }) {
        std::cout << "Reading " << path << std::endl;
        Mesh coralMesh;
        if(!readOBJ(path, coralMesh)) return 1;
        coralMeshes.push_back(coralMesh);
    }

    std::vector<Coral> corals;
    for(int i = 0; i < numberOfCorals; ++i) {
        double x = (double)rand() / RAND_MAX * 4.0;
        double y = 0.0;
        double z = (double)rand() / RAND_MAX * 4.0;
        Point_3 position(x, y, z);

        double rotation = (double)rand() / RAND_MAX * 2.0 * M_PI;

        int type = rand() % coralMeshes.size();

        corals.push_back( Coral(position, rotation, type) );
    }

    std::cout << "Generated " << numberOfCorals << " corals" << std::endl;

    Mesh combinedMesh = combineMeshes(corals);

    std::cout << "Combined " << numberOfCorals << " corals into one mesh" << std::endl;

    if(!writeOBJ("corals.obj", combinedMesh)) return 1;

    std::cout << "Wrote combined mesh to corals.obj" << std::endl;

    return 0;
}