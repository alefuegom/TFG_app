package alefuegom.tfg.model;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Entity
@Table(name="tratamientos")
public class Tratamiento extends BaseEntity{
	
	@NotBlank
	private String nombre;
	
	@NotBlank
	private String descipcion;
	
	private int precio;
	
	@NotNull
	private boolean abandono;
	
	private int horasAbandono;
	
	@ManyToOne(cascade= CascadeType.ALL)
	private Plaga plaga;

}
