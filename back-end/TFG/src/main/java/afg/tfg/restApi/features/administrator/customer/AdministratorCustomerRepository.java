package afg.tfg.restApi.features.administrator.customer;

import java.util.Collection;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import afg.tfg.restApi.model.Customer;

public interface AdministratorCustomerRepository extends CrudRepository<Customer, Integer>{

	@Query("SELECT c FROM Customer c")
	Collection<Customer> findAllCustomer();
}
