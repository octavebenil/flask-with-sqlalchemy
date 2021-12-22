from flask_testing import TestCase
from wsgi import app

class TestCrud(TestCase):
    
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_create_and_read_one_product(self):

        response = self.client.post("/api/v1/products", json={"name": "France3.fr"})

        self.assertEqual(response.status_code, 201)

        created_product = response.json

        #test read one product
        response = self.client.get("/api/v1/products/"+str(created_product["id"]))

        product = response.json

        #le product doit etre egal au produit qu'on vient de créer
        self.assertEqual(created_product, product)
        self.assertEqual(response.status_code, 200)


    def test_update_product(self):
        #on recupère tous les produits
        response = self.client.get("/api/v1/products")

        products = response.json

        #on va essayé de faire un mise à jour sur le premier produits obtenu
        if len(products) > 0:
            product_to_updated = products[0]

            updated_name = f"{product_to_updated['name']} updated"

            response = self.client.patch("/api/v1/products/"+str(product_to_updated["id"]), json={"name": updated_name})
            
            product_updated = response.json

            self.assertEqual(updated_name, product_updated["name"])
            self.assertEqual(response.status_code, 200)

    def test_update_validation_product(self):
        #on recupère tous les produits
        response = self.client.get("/api/v1/products")

        products = response.json

        #on va essayé de faire un mise à jour sur le premier produits obtenu
        if len(products) > 0:
            product_to_updated = products[0]

            #on essai de mettre a jour avec une valeur vide
            updated_name = ""

            response = self.client.patch("/api/v1/products/"+str(product_to_updated["id"]), json={"name": updated_name})

            self.assertEqual(response.status_code, 422)   


    def test_delete_product(self):
        #on recupère tous les produits
        response = self.client.get("/api/v1/products")

        products = response.json

        #on va essayé de faire un mise à jour sur le premier produits obtenu
        if len(products) > 0:
            product_to_delete = products[0]

            response = self.client.delete("/api/v1/products/"+str(product_to_delete["id"]), json={"id": product_to_delete["id"]})

            self.assertEqual(response.status_code, 204)

            #on regarde les produits si a dimunier
            response = self.client.get("/api/v1/products")
            after_delete = response.json

            self.assertGreater(len(products), len(after_delete))        
